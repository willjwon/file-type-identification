//
// Created by Jonghoon Won on 9/14/17.
//

#ifndef FILEFRAGMENTGENERATOR_PREPROCESS_HPP
#define FILEFRAGMENTGENERATOR_PREPROCESS_HPP

namespace baryberri {
    void preprocess(int* const& gramArray, double* const preprocessedArray, int arrayLength);
}


void baryberri::preprocess(int* const& gramArray, double* const preprocessedArray, int arrayLength) {
    // No Preprocessing: output the same value
    for (int i = 0; i < arrayLength; i++) {
        preprocessedArray[i] = gramArray[i];
    }

    // Example: Divison by 4kb(i.e. Getting Proportion)
    /*
    for (int i = 0; i < arrayLength; i++) {
        preprocessedArray[i] = gramArray[i] / 4096.0;
    }
     */
}

#endif //FILEFRAGMENTGENERATOR_PREPROCESS_HPP
