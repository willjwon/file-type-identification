# file-type-identification
File-Fragment Type Identification Using Deep Learning and other techniques

# Branch 관리 방법
본 프로젝트의 경우 다음과 같은 방법으로 branch를 관리하고자 합니다.
본 프로젝트에서는 master에 보호가 걸려 있어, master로 commit하는 것이 불가능합니다.
이에 의무적으로 branch를 통해 개발해야 하며, pull request를 통해 master로 변경 사항을 전달해야 합니다.
또한, pull request는 reviewer의 리뷰를 받기 전까지는 merge할 수 없도록 보호되어 있습니다. 이에 항상 pull request를 만드실 때, 상대방을 reviewer로 지정해 주시기 바랍니다.(reviewer는 label을 설정하는 곳 바로 위에 있습니다.)

이에, 아래와 같이 pull request, merge 및 rebase를 약속하는 것을 제안드립니다.
먼저, 아래와 같이 용어를 정의합니다.
1. master에서 분기하여 새로운 기능을 추가하는 branch를 **feature branch** 라고 하겠습니다. 예를 들어, 파일 조각을 만들어주는 `FileFragmentGenerator`을 개발하기 위한 `file-fragment-generator`을 들 수 있겠네요.
2. 'feature branch'에서 개발하는 프로그램에 새로운 기능을 추가하거나, 버그를 수정할 때 사용하는 branch를 **update-branch** 라고 하겠습니다. 예를 들어, `FileFragmentGenerator`이 one-hot encoding을 지원하도록 수정할 때, `one-hot` branch를 만들 수 있겠습니다.

이제, 아래와 같이 약속하고자 합니다.
1. 기능을 추가하는 **feature-branch** 는 master에 **merge** 합니다. 언제 기능을 추가하였는지가 중요한 정보이기 때문입니다.
2. update를 수행하는 **update-branch** 는 **feature-branch** 에 rebase합니다. **update-branch** 는 단순히 feature-branch를 보조하는 도구로서 사용되기 때문입니다. 

자세한 사항은 [wiki - Branch 관리 방법](https://github.com/baryberri/file-type-identification/wiki/Branch-관리-방법)을 참고해주시기 바랍니다.
