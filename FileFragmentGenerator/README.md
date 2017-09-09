# FileFragmentGenerator
이 프로그램은 folder별로 나누어진 특정 type의 파일들을 일정 수의 조각으로 나누어, 하나의 csv 파일에 기록하는 프로그램입니다.
이 프로그램은 C++로 작성되었으며, CMake 기반의 프로그램입니다.

## 사용법
1. FileFragmentGenerator에 들어 있는 `settings.json` 파일을 원하는 대로 수정합니다.
```json
{
    "fileType": ["html", "hwp", "pdf", "docx", "xlsx"],

    "inputDirectory": {
        "html": "./input/html",
        "hwp": "./input/hwp",
        "pdf": "./input/pdf",
        "docx": "./input/docx",
        "xlsx": "./input/xlsx"
    },

    "typeKey": {
        "html": 0,
        "hwp": 1,
        "pdf": 2,
        "docx": 3,
        "xlsx": 4
    },

    "outputDirectory": "./output",
    "outputFileName": "frequency_",

    "settings": {
        "gram": 1,
        "fragmentSize": 4096,
        "totalFragmentsPerType": 200000,
        "fragmentsPerCSV": 1000
    }
}

```

- 각 field에 대한 설명은 아래와 같습니다.
    * `fileType`: 조각으로 나누어야 할 파일들의 type을 기록합니다.
    *  `inputDirectory`: `fileType`에 지정된 type들의 파일들이 어떤 폴더에 위치하고 있는지를 기록합니다.
	`./`는 `settings.json` 파일이 위치한 폴더를 의미합니다.
    * `typeKey`: 각 `fileType`은 one-hot encoding을 통해 구분됩니다. 각 type의 몇 번째 bit가 1이 될 것인지 설정하시면 됩니다. **0부터 시작해서 순차적으로** 설정해주세요.
    * `outputDirectory`: 결과 csv가 기록될 위치를 지정합니다. 존재하지 않는 csv 파일 및 한 층의 폴더는 만들어주지만, 2개 이상의 폴더는 자동으로 만들어주지 않으니 주의해주시기 바랍니다. 또한, 프로그램을 재실행하면 덮어쓰기 모드로 실행되니, 폴더 내에 csv가 없도록 주의해주세요.
    * `outputFileName`: csv가 가질 fileName을 지정합니다. fileName 뒤에 연속적인 숫자가 자동으로 붙어 csv가 만들어집니다. 예를 들어, 이 field가 `frequency_`로 설정된 경우 `frequency_1.csv`의 csv 파일이 출력됩니다.
    * `settings`: 다음의 세 가지 설정을 지정합니다.
		* `gram`: 어떤 n-gram을 사용할 것인지를 지정합니다.
        만약 0으로 설정된 경우, frequency를 계산하지 않고, fragment 자체를 csv에 기록합니다.
		* `fragmentSize`: 파일 조각의 크기를 byte 단위로 기록합니다.
		* `totalFragmentsPerType`: 각 타입당 만들고 싶은 fragment의 갯수를 입력합니다. **총 fragment의 수가 아니라는** 것에 주의해주세요.
		* `fragmentsPerCSV`: 한 csv당 저장할 fragment의 수를 기록합니다.

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
