#include <iostream>
#include <fstream>
#include <sys/stat.h>
#include <ctime>
#include "json.hpp"
#include "FileManager.hpp"

using json = nlohmann::json;
using FileManager = baryberri::FileManager;

int main() {
    // start the timer
    std::clock_t startTime = clock();

    // Read and deserialize json settings
    json settings;
    std::ifstream settingsFile;
    settingsFile.open("./settings.json");
    settingsFile >> settings;
    FileManager::setSettings(&settings);

    // remove and remake the destination directory to make it clean.
    std::string inputDirectoryPath = settings["outputDirectory"];
    if (opendir(inputDirectoryPath.c_str()) == nullptr) {
            mkdir(inputDirectoryPath.c_str(), S_IRUSR | S_IWUSR | S_IXUSR | S_IRGRP | S_IXGRP | S_IROTH | S_IXOTH);
    }

    // Make fragments and save into csv file
    int numOfFragments = settings["settings"]["totalFragmentsPerType"];
    FileManager fileManager;
    while (fileManager.setToNextType()) {
        std::cout << "Generating fragments of type " << fileManager.getCurrentFileType() << " ..." << std::endl;
        fileManager.makeFragments(numOfFragments);
    }

    // close settings file
    settingsFile.close();

    // print the running time.
    std::clock_t endTime = clock();
    std::cout << std::fixed << std::setprecision(2)
              << "Total Running Time: " << (endTime - startTime) / CLOCKS_PER_SEC << "s" << std::endl;

    return 0;
}
