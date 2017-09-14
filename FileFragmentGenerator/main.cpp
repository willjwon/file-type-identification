#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <sys/stat.h>
#include "json.hpp"
#include "FileManager.hpp"
#include "Random.hpp"

using json = nlohmann::json;
using FileManager = baryberri::FileManager;
using baryberri::getRandom;


bool checkFragmentsLeft(const std::vector<int>& numOfFragmentsLeft);


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

    // check shuffling, and do the right stuff.
    bool shuffle = settings["shuffleOutput"];
    int numOfFragments = settings["settings"]["totalFragmentsPerType"];
    if (shuffle) {
        // Check how many file types have valid input files.
        std::vector<int> numOfFragmentsLeft;
        std::vector<FileManager*> fileManagers;

        FileManager defaultManager;
        while (defaultManager.setToNextType()) {
            std::cout << "Fragments of type " << defaultManager.getCurrentFileType() << " is available." << std::endl;
            fileManagers.push_back(new FileManager(defaultManager.getCurrentFileType()));
            numOfFragmentsLeft.push_back(numOfFragments);
        }

        // Make fragments and save.
        auto numOfValidTypes = (int) (numOfFragmentsLeft.size());
        int randomIndex = 0;

        std::cout << "Generating file fragments..." << std::endl;

        while (checkFragmentsLeft(numOfFragmentsLeft)) {
            do {
                randomIndex = getRandom(0, numOfValidTypes);
            } while (numOfFragmentsLeft[randomIndex] == 0);
            fileManagers[randomIndex]->makeFragment();
            numOfFragmentsLeft[randomIndex]--;
        }
    } else {
        std::cout << "sequential!" << std::endl;
        FileManager fileManager;
        while (fileManager.setToNextType()) {
            fileManager.makeFragments(numOfFragments);
        }
    }

    // close settings file
    settingsFile.close();

    // print the running time.
    std::clock_t endTime = clock();
    std::cout << "Fragment generation is done." << std::endl;
    std::cout << std::fixed << std::setprecision(2)
              << "Total Running Time: " << (double)(endTime - startTime) / CLOCKS_PER_SEC << "s" << std::endl;

}


bool checkFragmentsLeft(const std::vector<int>& numOfFragmentsLeft) {
    for (const int leftFragment : numOfFragmentsLeft) {
        if (leftFragment != 0) {
            return true;
        }
    }
    return false;
}
