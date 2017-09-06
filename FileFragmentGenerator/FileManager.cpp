#include <dirent.h>
#include <iostream>
#include <vector>
#include "FileManager.hpp"


json* baryberri::FileManager::settings = nullptr;
int baryberri::FileManager::numOfFileTypes = 0;
std::string baryberri::FileManager::outputBasePath = "";
int baryberri::FileManager::currentOutputFileNumber = 0;
std::ifstream baryberri::FileManager::inputFileStream;
std::ofstream baryberri::FileManager::outputFileStream;

baryberri::FileManager::FileManager() {
    std::vector<std::string> fileTypes = (*settings)["fileType"];

    currentFileTypeIndex = -1;
    currentDirectory = nullptr;
    baseOffset = 0;
    currentFileOffset = 0;
    gramSize = (*settings)["settings"]["gram"];
    fragmentSize = (*settings)["settings"]["fragmentSize"];
    numOfFragmentsPerCSV = (*settings)["settings"]["fragmentsPerCSV"];
    currentFile = nullptr;
    numOfFileTypes = (int)(fileTypes.size());

    std::string outputDirectory = (*settings)["outputDirectory"];
    if (!has_suffix(outputDirectory, "/")) {
        outputDirectory += "/";
    }
    std::string outputBaseFileName = (*settings)["outputFileName"];
    outputBasePath = outputDirectory + outputBaseFileName;

    initializeFile();
}

baryberri::FileManager::FileManager(const std::string& fileType) {
    std::vector<std::string> fileTypes = (*settings)["fileType"];
    auto inputDirectories = (*settings)["inputDirectory"];

    currentFileType = fileType;
    currentFileTypeIndex = (int) (std::find(fileTypes.begin(), fileTypes.end(), fileType) - fileTypes.begin());
    currentInputDirectoryPath = inputDirectories[fileType];
    currentDirectory = opendir(currentInputDirectoryPath.c_str());
    baseOffset = 0;
    currentFileOffset = 0;
    gramSize = (*settings)["settings"]["gram"];
    fragmentSize = (*settings)["settings"]["fragmentSize"];
    numOfFragmentsPerCSV = (*settings)["settings"]["fragmentsPerCSV"];
    numOfFileTypes = (int)(fileTypes.size());

    std::string outputDirectory = (*settings)["outputDirectory"];
    if (!has_suffix(outputDirectory, "/")) {
        outputDirectory += "/";
    }
    std::string outputBaseFileName = (*settings)["outputFileName"];
    outputBasePath = outputDirectory + outputBaseFileName;

    initializeFile();
}

baryberri::FileManager::~FileManager() {
    if (currentDirectory != nullptr) {
        closedir(currentDirectory);
    }

    if (inputFileStream.is_open()) {
        inputFileStream.close();
    }

    if (outputFileStream.is_open()) {
        outputFileStream.close();
    }
}

const std::string& baryberri::FileManager::getCurrentFileType() {
    return currentFileType;

}

const bool baryberri::FileManager::isDirectoryExist() {
    return currentDirectory != nullptr;
}

const bool baryberri::FileManager::setToNextType() {
    std::vector<std::string> fileTypes = (*settings)["fileType"];
    auto inputDirectories = (*settings)["inputDirectory"];

    currentFileTypeIndex++;
    if (currentFileTypeIndex >= numOfFileTypes) {
        return false;
    }

    if (currentDirectory != nullptr) {
        closedir(currentDirectory);
    }

    currentFileType = fileTypes[currentFileTypeIndex];
    currentInputDirectoryPath = inputDirectories[currentFileType];
    currentDirectory = opendir(currentInputDirectoryPath.c_str());

    if (!isDirectoryExist()) {
        if (!setToNextType()) {
            return false;
        };
    }

    setToNextFile();

    return true;
}

void baryberri::FileManager::makeFragment() {
    static int numOfFragmentsGenerated = 0;
    auto* fragmentArray = new char[fragmentSize];
    getFragment(fragmentArray);
    if (gramSize == 0) {
        saveRawFragmentData(fragmentArray);
    } else {
        auto* gramArray = new int[int(pow(2, 8 * gramSize))];
        computeNgram(fragmentArray, gramArray);
        saveGramData(gramArray);
    }

    if ((++numOfFragmentsGenerated) % numOfFragmentsPerCSV == 0) {
        changeToNextOutputFile();
    }

}

void baryberri::FileManager::makeFragments(const int fragmentNumber) {
    for (int i = 0; i < fragmentNumber; i++) {
        makeFragment();
    }
}

void baryberri::FileManager::setSettings(json* settings) {
    FileManager::settings = settings;
}

void baryberri::FileManager::rewindFile() {
    if (currentDirectory != nullptr) {
        rewinddir(currentDirectory);
    }
}

bool baryberri::FileManager::initializeFile() {
    if (!outputFileStream.is_open()) {
        changeToNextOutputFile();
    }

    if (inputFileStream.is_open()) {
        inputFileStream.close();
    }

    inputFilePath = getNextFilePath();
    if (inputFilePath.empty()) {
        return false;
    }

    inputFileStream.open(inputFilePath);
    return true;
}

void baryberri::FileManager::setToNextFile() {
    if (inputFileStream.is_open()) {
        inputFileStream.close();
    }

    inputFilePath = getNextFilePath();
    if (inputFilePath.empty()) {
        rewindFile();
        setToNextOffset();
        inputFilePath = getNextFilePath();
    }
    currentFileOffset = baseOffset;
    inputFileStream.open(inputFilePath);
}

const std::string baryberri::FileManager::getNextFilePath() {
    if (currentDirectory == nullptr) {
        return "";
    }

    do {
        currentFile = readdir(currentDirectory);
        if (currentFile == nullptr) {
            return "";
        }
    } while (!has_suffix(currentFile->d_name, "." + currentFileType));

    std::string path = currentInputDirectoryPath;
    if (!has_suffix(currentInputDirectoryPath, "/")) {
        path += "/";
    }
    path += currentFile->d_name;
    return path;
}


void baryberri::FileManager::getFragment(char* fragmentArray) {
    reloadInputStream();
    inputFileStream.read(fragmentArray, fragmentSize);
    currentFileOffset += fragmentSize;
    if (inputFileStream.gcount() < fragmentSize) {
        setToNextFile();
        getFragment(fragmentArray);
    }
}

void baryberri::FileManager::saveRawFragmentData(char* const& fragmentArray) {
    for (int i = 0; i < fragmentSize; i++) {
        outputFileStream << int((unsigned char)(fragmentArray[i])) << ",";
    }
    int fileTypeKey = (*settings)["typeKey"][currentFileType];
    for (int i = 0; i < numOfFileTypes; i++) {
        if (i == fileTypeKey) {
            outputFileStream << 1;
        } else {
            outputFileStream << 0;
        }
        if (i != numOfFileTypes - 1) {
            outputFileStream << ",";
        } else {
            outputFileStream << std::endl;
        }
    }
}

void baryberri::FileManager::computeNgram(char* const& fragmentArray, int* gramArray) {
    for (int i = 0; i < int(pow(2, 8 * gramSize)); i++) {
        gramArray[i] = 0;
    }

    for (int i = fragmentSize - 1; i >= gramSize - 1; i--) {
        int gramValue = 0;
        int digit = 1;
        for (int j = 0; j < gramSize; j++) {
            gramValue += digit * (unsigned char)(fragmentArray[i - j]);
            digit *= 256;
        }
        gramArray[gramValue]++;
    }
}

void baryberri::FileManager::saveGramData(int* const & gramArray) {
    for (int i = 0; i < int(pow(2, 8 * gramSize)); i++) {
        outputFileStream << gramArray[i] << ",";
    }
    int fileTypeKey = (*settings)["typeKey"][currentFileType];
    for (int i = 0; i < numOfFileTypes; i++) {
        if (i == fileTypeKey) {
            outputFileStream << 1;
        } else {
            outputFileStream << 0;
        }
        if (i != numOfFileTypes - 1) {
            outputFileStream << ",";
        } else {
            outputFileStream << std::endl;
        }
    }
}

void baryberri::FileManager::setToNextOffset() {
    // offset has `(numerator / denominator) * fragmentSize` format.
    static int numerator = 1;
    static int denominator = 2;

    baseOffset = int(((double)numerator / (double)denominator) * fragmentSize);

    numerator += 2;
    if (numerator >= denominator) {
        numerator = 1;
        denominator *= 2;
    }
}
void baryberri::FileManager::reloadInputStream() {
    if (inputFileStream.is_open()) {
        inputFileStream.close();
    }

    inputFileStream.open(inputFilePath, std::fstream::app);
    inputFileStream.seekg(currentFileOffset);
}

const bool baryberri::FileManager::has_suffix(const std::string& str, const std::string& suffix) {
    return str.size() >= suffix.size()
            && str.compare(str.size() - suffix.size(), suffix.size(), suffix) == 0;
}

void baryberri::FileManager::changeToNextOutputFile() {
    if (outputFileStream.is_open()) {
        outputFileStream.close();
    }

    std::string newOutputPath = outputBasePath + std::to_string(++currentOutputFileNumber) + ".csv";
    outputFileStream.open(newOutputPath, std::fstream::app);
}