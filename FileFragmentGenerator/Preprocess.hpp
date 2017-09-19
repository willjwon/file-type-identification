//.';]\\\\\\\\\\\
// Created by Jonghoon Won on 9/14/17.
//

#ifndef FILEFRAGMENTGENERATOR_PREPROCESS_HPP
#define FILEFRAGMENTGENERATOR_PREPROCESS_HPP

#include <cmath>

namespace baryberri {
    void preprocess(int* const& gramArray, double* const preprocessedArray, int arrayLength);
}


void baryberri::preprocess(int* const& gramArray, double* const preprocessedArray, int arrayLength) {
    // No Preprocessing: output the same value
//    for (int i = 0; i < arrayLength; i++) {
//        preprocessedArray[i] = gramArray[i];
//    }

    // Example: Division by 4kb(i.e. Getting Proportion)
    /*
    for (int i = 0; i < arrayLength; i++) {
        preprocessedArray[i] = gramArray[i] / 4096.0;
    }
     */

    // Companding by Mu-Law
    // 1. Finding the most frequent byte value
    int max_frequency = 1;
    for (int i = 0; i < arrayLength; i++) {
        if (gramArray[i] > max_frequency) {
            max_frequency = gramArray[i];
        }
    }

    // 2. Normalize and apply Mu-law
    double normalized_frequency = 0;
    for (int i = 0; i < arrayLength; i++) {
        normalized_frequency = gramArray[i] / max_frequency;
        preprocessedArray[i] = log(1 + 256 * normalized_frequency) / log(1 + 256);
    }

}

#endif //FILEFRAGMENTGENERATOR_PREPROCESS_HPP
