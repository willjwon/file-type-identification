#include <iostream>
#include "FragmentManager.hpp"

std::string baryberri::FragmentManager::outputFilePath = "";

baryberri::FragmentManager::FragmentManager(FileManager* fileManager, json* settings) {
    this->settings = settings;
    this->fileManager = fileManager;

    offset = 0;
    gramSize = (*settings)["settings"]["gram"];
    fragmentSize = (*settings)["settings"]["fragmentSize"];
}

baryberri::FragmentManager::~FragmentManager() {
    if (currentFileStream.is_open()) {
        currentFileStream.close();
    }

    if (outputCSVStream.is_open()) {
        outputCSVStream.close();
    }
}

void baryberri::FragmentManager::generateFragment(const int fragmentNumber) {
    for (int i = 0; i < fragmentNumber; i++) {
        getAndSaveFragment();
    }
}

void baryberri::FragmentManager::getAndSaveFragment() {
    auto* fragmentArray = new char[fragmentSize];
    getFragment(fragmentArray);

    if (gramSize == 0) {
        saveRawFragmentDataIntoCSV(fragmentArray);
    } else {
        auto* gramArray = new int[int(pow(2, 8 * gramSize))];
        for (int i = 0; i < int(pow(2, 8 * gramSize)); i++) {
            gramArray[i] = 0;
        }
        computeNgram(fragmentArray, gramArray);
        saveGramDataIntoCSV(gramArray);
    }
}

void baryberri::FragmentManager::changeOutputFilePath(const std::string& newOutputFilePath) {
    outputFilePath = newOutputFilePath;
}

void baryberri::FragmentManager::changeToNewOutputFile() {
    if (outputCSVStream.is_open()) {
        outputCSVStream.close();
    }
    outputCSVStream.open(outputFilePath, std::fstream::app);
}

void baryberri::FragmentManager::setToNextFile() {
    if (currentFileStream.is_open()) {
        currentFileStream.close();
    }
    std::string nextFilePath = (*fileManager).getNextFilePath();
    if (nextFilePath.empty()) {
        (*fileManager).rewindFile();
        setToNextOffset();
        nextFilePath = (*fileManager).getNextFilePath();
    }

    currentFileStream.open(nextFilePath);
    currentFileStream.seekg(offset);
}

void baryberri::FragmentManager::getFragment(char* fragmentArray) {
    currentFileStream.read(fragmentArray, fragmentSize);
    if (currentFileStream.gcount() < fragmentSize) {
        setToNextFile();
        currentFileStream.read(fragmentArray, fragmentSize);
    }
}

void baryberri::FragmentManager::computeNgram(char* const& fragmentArray, int* gramArray) {
    for (int i = 0; i < fragmentSize; i++) {
        gramArray[int((unsigned char)(fragmentArray[i]))]++;
    }
}

void baryberri::FragmentManager::saveRawFragmentDataIntoCSV(char* const& fragmentArray) {

    for (int i = 0; i < fragmentSize; i++) {
        outputCSVStream << int((unsigned char)(fragmentArray[i])) << ",";
    }
    int fileTypeKey = (*settings)["typeKey"][(*fileManager).getCurrentFileType()];
    int numOfFileTypes = (*fileManager).getNumOfFileTypes();
    for (int i = 0; i < numOfFileTypes; i++) {
        if (i == fileTypeKey) {
            outputCSVStream << 1;
        } else {
            outputCSVStream << 0;
        }
        if (i != numOfFileTypes - 1) {
            outputCSVStream << ",";
        } else {
            outputCSVStream << std::endl;
        }
    }
}

void baryberri::FragmentManager::saveGramDataIntoCSV(int* const & gramArray) {
    for (int i = 0; i < int(pow(2, 8 * gramSize)); i++) {
        outputCSVStream << gramArray[i] << ",";
    }
    int fileTypeKey = (*settings)["typeKey"][(*fileManager).getCurrentFileType()];
    int numOfFileTypes = (*fileManager).getNumOfFileTypes();
    for (int i = 0; i < numOfFileTypes; i++) {
        if (i == fileTypeKey) {
            outputCSVStream << 1;
        } else {
            outputCSVStream << 0;
        }
        if (i != numOfFileTypes - 1) {
            outputCSVStream << ",";
        } else {
            outputCSVStream << std::endl;
        }
    }
}



void baryberri::FragmentManager::setToNextOffset() {
    // offset has `(numerator / denominator) * fragmentSize` format.
    static int numerator = 1;
    static int denominator = 2;

    offset = int(((double)numerator / (double)denominator) * fragmentSize);

    numerator += 2;
    if (numerator >= denominator) {
        numerator = 1;
        denominator *= 2;
    }
}
