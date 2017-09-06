#include <iostream>
#include <iomanip>
#include <fstream>
#include <sys/stat.h>
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
    std::vector<int> numOfFragmentsLeft;
    std::vector<FileManager*> fileManagers;

    FileManager defaultManager;
    while (defaultManager.setToNextType()) {
        std::cout << "Generating fragments of type " << defaultManager.getCurrentFileType() << " ..." << std::endl;
        fileManagers.push_back(new FileManager(defaultManager.getCurrentFileType()));
        numOfFragmentsLeft.push_back(numOfFragments);
//        defaultManager.makeFragments(numOfFragments);
    }
    std::cout << defaultManager.setToNextType() << std::endl;

    std::cout << fileManagers.size() << " " << numOfFragmentsLeft.size() << std::endl;

    // close settings file
    settingsFile.close();

    // print the running time.
    std::clock_t endTime = clock();
    std::cout << std::fixed << std::setprecision(2)
              << "Total Running Time: " << (double)(endTime - startTime) / CLOCKS_PER_SEC << "s" << std::endl;

    return 0;
}
