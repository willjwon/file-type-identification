#include <dirent.h>
#include <iostream>
#include "FileManager.hpp"

baryberri::FileManager::FileManager(json *settings) {
    this->settings = settings;
}

baryberri::FileManager::~FileManager() {
    if (currentDirectory != nullptr) {
        closedir(currentDirectory);
    }
}

const std::string baryberri::FileManager::getCurrentFileType() {
    return currentFileType;
}

const bool baryberri::FileManager::isDirectoryExist() {
    return currentDirectory != nullptr;
}

const bool baryberri::FileManager::setToNextFileType() {
    static int currentlySelectedFileType = -1;

    auto fileTypes = (*settings)["fileType"];
    auto inputDirectories = (*settings)["inputDirectory"];

    if (currentDirectory != nullptr) {
        closedir(currentDirectory);
    }

    currentlySelectedFileType++;
    bool notOverflowed = true;
    if (currentlySelectedFileType >= fileTypes.size()) {
        notOverflowed = false;
        currentlySelectedFileType = 0;
    }

    currentFileType = fileTypes[currentlySelectedFileType];
    std::string inputDirectory = inputDirectories[currentFileType];
    currentInputDirectoryPath = inputDirectory;
    currentDirectory = opendir(inputDirectory.c_str());

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