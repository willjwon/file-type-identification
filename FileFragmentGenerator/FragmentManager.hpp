#ifndef FILEFRAGMENTGENERATOR_FRAGMENTMANAGER_HPP
#define FILEFRAGMENTGENERATOR_FRAGMENTMANAGER_HPP

#include <fstream>
#include "json.hpp"
#include "FileManager.hpp"

using json = nlohmann::json;

namespace baryberri {
    class FragmentManager;
}

class baryberri::FragmentManager {
public:
    /// Construct FragmentManager with given FileManager.
    ///
    /// \param fileManager a FileManager pointer to use
    /// \param settings a json settings file
    explicit FragmentManager(FileManager* fileManager);

    /// Destruct FragmentManager, makes sure currentFileStream is closed before object destruction.
    ~FragmentManager();

    /// make the given number of fragments, and save it into .csv file.
    ///
    /// \param fragmentNumber wanted number of fragments to generate
    /// \returns true if file fragments are well-generated, otherwise returns false
    void generateFragment(const int fragmentNumber);

    /// get a fragment, and save it into csv file located by json settings.
    void getAndSaveFragment();

    /// Change outputFilePath to new outputFilePath.
    ///
    /// \param newOutputFilePath new ouputFilepath to set
    static void changeOutputFilePath(const std::string& newOutputFilePath);

    /// update outputCSVStream to new outputFilePath.
    void changeToNewOutputFile();

private:
    json* settings;
    FileManager* fileManager;
    std::ifstream currentFileStream;
    std::ofstream outputCSVStream;
    int offset;
    int gramSize;
    int fragmentSize;
    static std::string outputFilePath;

    /// set currentFileStream to next file.
    void setToNextFile();

    /// read a new fragment in currentFileStream, and save it into fragmentArray.
    void getFragment(char* fragmentArray);

    /// save raw data read by getFragment into csv file
    void saveRawFragmentDataIntoCSV(char* const& fragmentArray);

    /// compute n-gram frequency data from fragmentArray, and save it into gramArray.
    void computeNgram(char* const& fragmentArray, int* gramArray);

    /// save n-gram data into csv file.
    void saveGramDataIntoCSV(int* const& gramArray);

    /// set offset to next available offset.
    void setToNextOffset();
};

#endif //FILEFRAGMENTGENERATOR_FRAGMENTMANAGER_HPP
