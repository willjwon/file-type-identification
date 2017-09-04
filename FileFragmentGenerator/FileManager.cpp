#include <dirent.h>
#include <iostream>
#include <vector>
#include "FileManager.hpp"

using json = nlohmann::json;

int baryberri::FileManager::numOfFileTypes = 0;
bool baryberri::FileManager::numOfFileTypesHasSet = false;
static json* settings = nullptr;

baryberri::FileManager::FileManager() {
    if (!numOfFileTypesHasSet) {
        numOfFileTypesHasSet = true;
        std::vector<std::string> fileTypes = (*settings)["fileType"];
        numOfFileTypes = (int)fileTypes.size();
    }
}

baryberri::FileManager::~FileManager() {
    if (currentDirectory != nullptr) {
        closedir(currentDirectory);
    }
}

void baryberri::FileManager::setSettings(json* settings) {
    this->settings = settings;
}

void baryberri::FileManager::setToFileType(std::string fileType) {
    std::string inputDirectory = (*settings)["inputDirectory"][fileType];

    if (currentDirectory != nullptr) {
        closedir(currentDirectory);
    }

    currentInputDirectoryPath = inputDirectory;
    currentDirectory = opendir(inputDirectory.c_str());
}

void baryberri::FileManager::setToFilePath(std::string directoryPath) {
    if (currentDirectory != nullptr) {
        closedir(currentDirectory);
    }

    currentDirectory = opendir(directoryPath.c_str());
}

const std::string baryberri::FileManager::getCurrentFileType() {
    return currentFileType;
}

const int baryberri::FileManager::getNumOfFileTypes() {
    return numOfFileTypes;
}

const json* baryberri::FileManager::getSettings() {
    return settings;
}

const bool baryberri::FileManager::isDirectoryExist() {
    return currentDirectory != nullptr;
}

const bool baryberri::FileManager::setToNextFileType(bool reset) {
    static int currentlySelectedFileType = -1;

    auto fileTypes = (*settings)["fileType"];
    auto inputDirectories = (*settings)["inputDirectory"];

    if (currentDirectory != nullptr) {
        closedir(currentDirectory);
    }

    bool notOverflowed = true;
    if (reset) {
        currentlySelectedFileType = -1;
    } else {
        currentlySelectedFileType++;

        if (currentlySelectedFileType >= fileTypes.size()) {
            notOverflowed = false;
            currentlySelectedFileType = 0;
        }
        currentFileType = fileTypes[currentlySelectedFileType];
        std::string inputDirectory = inputDirectories[currentFileType];
        currentInputDirectoryPath = inputDirectory;
        currentDirectory = opendir(inputDirectory.c_str());
    }

    return notOverflowed;
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

void baryberri::FileManager::rewindFile() {
    if (currentDirectory != nullptr) {
        rewinddir(currentDirectory);
    }
}

const bool baryberri::FileManager::has_suffix(const std::string& str, const std::string& suffix) {
    return str.size() >= suffix.size()
            && str.compare(str.size() - suffix.size(), suffix.size(), suffix) == 0;
}