#include <iostream>
#include <fstream>
#include "json.hpp"
#include "FileManager.hpp"
#include "FragmentManager.hpp"

using json = nlohmann::json;
using FileManager = baryberri::FileManager;
using FragmentManager = baryberri::FragmentManager;

int main() {
    // Read and deserialize json settings
    json settings;
    std::ifstream settingsFile;
    settingsFile.open("./settings.json");
    settingsFile >> settings;

    // Remove csv file if one already exists.
    std::string outputPath = settings["outputCSV"];
    remove(outputPath.c_str());

    // Make fragments and save into csv file
    int numOfFragments = settings["settings"]["numOfFragments"];
    FileManager fileManager(&settings);
    while (fileManager.setToNextFileType()) {
        if (fileManager.isDirectoryExist()) {
            std::cout << "Generating fragments of type " << fileManager.getCurrentFileType() << " ..." << std::endl;
            FragmentManager fragmentManager(&fileManager, &settings);
            fragmentManager.generateFragment(numOfFragments);
        }
    }

    // close settings file
    settingsFile.close();

    return 0;
}
