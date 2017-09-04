#ifndef FILEFRAGMENTGENERATOR_FILEMANAGER_HPP
#define FILEFRAGMENTGENERATOR_FILEMANAGER_HPP

#include <dirent.h>
#include "json.hpp"

using json = nlohmann::json;

namespace baryberri {
    class FileManager;
}

class baryberri::FileManager {
public:
    /// create a new FileManager with given json settings.
    /// as it doesn't call setToNextFileType automatically, it should be called manually.
    ///
    /// \param settings json settings file to use
    explicit FileManager(json* settings);

    /// close the directory before FileManager destructs.
    ~FileManager();

    /// set a FileManager to a specific given type.
    ///
    /// \param fileType fileType to set
    void setToFileType(std::string fileType);


    /// set a FileManager to a specific given directory path.
    ///
    /// \param directoryPath directory's path to set
    void setToFilePath(std::string directoryPath);

    /// get currentFileType.
    ///
    /// \return currentFileType
    const std::string getCurrentFileType();

    /// get numOfFileTypes;
    ///
    /// \return numOfFileTypes;
    static const int getNumOfFileTypes();

    /// Returns is directory of given file type exists, and well-opened.
    ///
    /// \return true if directory exists and opened, otherwise false.
    const bool isDirectoryExist();

    /// change currentFileType and currentTypesInputDirectoryPath to next available file type.
    ///
    /// \return false if there's no next file type available, else returns true.
    const bool setToNextFileType();

    /// gets an available file's path inside currentTypesInputDirectoryPath.
    /// the file is checked whether it has same corresponding extension with currentFileType.
    ///
    /// \return a file's path, if available. If there's no file available, returns empty string.
    const std::string getNextFilePath();

    /// reset the currentFile and restart iterating current directory.
    void rewindFile();

private:
    /// json settings file that's loaded.
    json* settings;

    /// settings has "fileType": ["html", "hwp", "pdf", "docx", "xlsx"] field.
    /// currentFileType indicates currently selected file type.
    std::string currentFileType;

    /// current input directory path, like "./hwp/"
    std::string currentInputDirectoryPath;

    /// indicates the current directory.
    DIR* currentDirectory;

    /// indicates the current file.
    struct dirent* currentFile;

    /// get how many file types exist.
    static int numOfFileTypes;

    /// checks whether given str has a given suffix.
    /// \param str string to test whether it has given suffix or not
    /// \param suffix suffix string to test
    /// \return true if given str has given suffix, otherwise false.
    static const bool has_suffix(const std::string& str, const std::string& suffix);
};

#endif //FILEFRAGMENTGENERATOR_FILEMANAGER_HPP
