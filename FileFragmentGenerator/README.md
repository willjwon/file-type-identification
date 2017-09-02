# FileFragmentGenerator
이 프로그램은 folder별로 나누어진 특정 type의 파일들을 일정 수의 조각으로 나누어, 하나의 csv 파일에 기록하는 프로그램입니다.
이 프로그램은 C++로 작성되었으며, CMake 기반의 프로그램입니다.

## 사용법
1. FileFragmentGenerator에 들어 있는 `settings.json` 파일을 원하는 대로 수정합니다.
```json
{
    "fileType": ["html", "hwp", "pdf", "docx", "xlsx"],

    "inputDirectory": {
        "html": "./html",
        "hwp": "./hwp",
        "pdf": "./pdf",
        "docx": "./docx",
        "xlsx": "./xlsx"
    },

    "typeKey": {
        "html": 0,
        "hwp": 1,
        "pdf": 2,
        "docx": 3,
        "xlsx": 4
    },

    "outputCSV": "../frequency.csv",

    "settings": {
        "gram": 1,
        "fragmentSize": 4096,
        "numOfFragments": 50000
    }
}
```

- 각 field에 대한 설명은 아래와 같습니다.
    * `fileType`: 조각으로 나누어야 할 파일들의 type을 기록합니다.
    *  `inputDirectory`: `fileType`에 지정된 type들의 파일들이 어떤 폴더에 위치하고 있는지를 기록합니다.
	`./`는 `settings.json` 파일이 위치한 폴더를 의미합니다.
    * `typeKey`: 각 `fileType` 마다 일정한 key가 csv의 row의 맨 마지막에 기록됩니다. 각 type이 가져야 하는 key를 지정합니다.
    * `outputCSV`: 결과 csv가 기록될 위치를 지정합니다. `../`는 상위 폴더를 의미합니다. 존재하지 않는 csv 파일은 만들어주지만, 존재하지 않는 폴더는 자동으로 만들어주지 않으니, 꼭 존재하는 폴더로 설정해야 합니다.
    * `settings`: 다음의 세 가지 설정을 지정합니다.
		* `gram`: 어떤 n-gram을 사용할 것인지를 지정합니다.
        만약 0으로 설정된 경우, frequency를 계산하지 않고, fragment 자체를 csv에 기록합니다.
		* `fragmentSize`: 파일 조각의 크기를 byte 단위로 기록합니다.
		* `numOfFragments`: 각 파일 type별로 만들고자 하는 fragment의 갯수를 지정합니다.

2. 프로젝트를 빌드하고 실행합니다. 한 번 빌드한 후에 `settings.json` 파일만 수정했다면, 새로 build할 필요 없이 4번과 같이 실행만 하면 됩니다.
- CMake는 Unix의 Makefile을 자동으로 만들어주는 프로그램입니다. 이렇게 만들어진 Makefile을 사용하여, make 명령어를 통해 프로젝트를 컴파일할 수 있습니다.
    1. CMake가 없다면 아래의 명령어를 따라 homebrew를 통해 cmake를 설치합니다.
        ```bash
        $ brew install cmake
        ```
    2. cmake를 통해 Makefile을 만듭니다.
        ```bash
        $ cd FileFragmentGenerator
        $ cmake .
        ```
    3. 만들어진 Makefile과 make 명령어를 통해 프로젝트를 build합니다.
        ```bash
        $ make
        ```
    4. 컴파일된 프로그램을 실행합니다. 실행 전에 `settings.json`에서 설정한 폴더에 fragment를 만들 파일들을 위치시켰는지 확인해주세요.
        ```bash
        $ ./FileFragmentGenerator
        ```

### 참고
이 프로그램은 다음의 C++용 JSON Parsing API를 사용했습니다. [nlohmann/json](https://github.com/nlohmann/json)
