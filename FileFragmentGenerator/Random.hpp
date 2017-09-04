#ifndef FILEFRAGMENTGENERATOR_RANDOM_HPP
#define FILEFRAGMENTGENERATOR_RANDOM_HPP

#include <random>

namespace baryberri {
    /// get a random number between start and end, where end is exclusive.
    /// \param start
    /// \param end
    /// \return a random number between start..<end.
    int getRandom(int start, int end);
}

int baryberri::getRandom(int start, int end) {
    static std::random_device randomDevice;
    static std::mt19937 mt(randomDevice());
    static std::uniform_real_distribution<double> distribution(0, 1);

    return (int)(start + distribution(mt) * (end - start));
}

#endif //FILEFRAGMENTGENERATOR_RANDOM_HPP
