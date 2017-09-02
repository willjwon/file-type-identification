# file-type-identification
File-Fragment Type Identification Using Deep Learning and other techniques

# Branch 관리 방법
아래와 같은 방법으로 branch를 관리하고자 합니다. (Git 사용 방법 연습 차원에서)

## Merge vs. Rebase
Git에서는 branch를 사용하여 다른 사람의 개발을 방해하지 않으면서 새로운 개발 stream을 만들 수 있습니다.
이렇게 개발한 branch를 다른 사람의 작업과 합칠 때는, merge와 rebase라는 두 가지의 기법 중 하나를 사용합니다.
![merge-rebase](https://raw.githubusercontent.com/gitforteams/diagrams/master/balsamiq/merge-types.png "merge and rebase")

위 그림의 경우, 분홍색 branch 맨 왼쪽의 master 커밋에서 분기를 시작해, 자신만의 개발 작업을 시작했습니다.
그 동안 파란색의 master branch는 두 개의 커밋 업데이트가 더 있었습니다.
분홍색 branch는 자신의 작업을 master의 작업과 합치려고 합니다.

1. 이 때 merge를 사용하면, 그림의 왼쪽과 같이 master와 분홍색의 변경 사항이 모두 반영된 새로운 'merge commit'이 만들어집니다.
따라서, log에 '분기와 합침'이 일어난 대로 정확히 기록되게 됩니다.

2. rebase는 이와 다른 과정을 거칩니다. 그림의 오른쪽을 참고하세요.
rebase란 말 그대로 're-base'로서, branch가 자신이 분기하기 시작한 commit을 변경하는 작업을 의미합니다.
분홍색 branch가 'master로 rebase' 명령어를 수행하면, 분홍색 branch는 master의 첫 번째 커밋이 아닌, 최신 커밋에서 분기가 시작된 것으로 변경됩니다. 
(분홍색이 분기한 이후 master에도 두 개의 커밋에 의해 변경 사항이 있었습니다. 이 변경 사항들을 분홍색의 첫 번째 commit부터 적용시켜, 마치 분홍색 branch가 master의 최신 커밋에서 분기한 것처럼 변경시키는 것입니다.)

이렇게 분홍색 branch를 master로 rebase시킨 후 merge를 수행하게 되면, git는 새로운 merge 커밋을 만들지 않습니다.
master을 분홍 branch와 merge하라는 명령을 내렸을 때, 왼쪽 그림은 merge commit을 만들었습니다. 이와는 달리, 오른쪽 그림의 경우 git의 입장에서 변경은 한 줄로 이루어졌으므로, 새로운 merge commit은 만들어지지 않고 단순히 개발이 한 줄로 이루어진 것처럼 표현되게 됩니다.

3. 따라서, 비록 같은 branch에서 같은 개발을 거쳤더라도, 
    * '내가 어디에서 분기해서, 어디에서 합쳤다'라는 정보가 중요할 경우는 merge를, 
    * '비록 여러 branch에서 개발했더라도, 하나의 branch에서 개발한 것처럼' 맥락을 유지해야 하는 경우는 rebase를 사용하게 됩니다.

## 본 프로젝트의 경우
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

## 예시
`FileFragmentGenerator`를 만드는 경우를 예시로서 보여드리겠습니다.
1. 바버는 새로운 기능을 추가할 `file-fragment-generator` **feature-branch** 를 만듭니다. 이 branch는 현재의 최신 master 커밋에서 분기합니다.
    ```bash
    # git branch (새 branch) (기반 commit)
    $ git branch file-fragment-generator master
    $ git checkout file-fragment-generator
    ```

2. 기능을 모두 추가한 바버는 `file-fragment-generator branch`를 푸시한 후 pull request를 보내고, 컁님이 이를 merge합니다.
    ```bash
    # git push (remote) (remote의 도착 branch)
    $ git checkout file-fragment-generator
    $ git push origin file-fragment-generator
    ```
    * 바버: Pull request
    * 컁님: **Merge**

3. 컁님은 바버에게 one-hot encoding 기능이 필요하다는 issue를 올립니다. 바버는 `file-fragment-generator` 에 기능을 추가하면서도, 현재의 `file-fragment-generator`이 망가지는 것은 원하지 않기 때문에 새로운 branch인 `one-hot` branch를 만듭니다. 이 branch는 단순히 개발용이므로 서버에 푸시하지 않고, 바버만이 local에서 사용합니다. 또한, 이 branch는 당연히 분기 지점이 master이 아닌, 현재의 최신 `file-fragment-generator` 커밋입니다.
    ```bash
    $ git branch one-hot file-fragment-generator
    $ git checkout one-hot
    ```

4. 바버는 one-hot branch에서 one-hot encoding 기능을 구현했고, 충분한 테스트도 완료했습니다. 이제, 이 변경 사항을 서버에 반영하고자 합니다. 바버가 원하는 것은 바버가 비록 `one-hot` branch에서 개발했더라도 마치 `file-fragment-generator` branch에서 쭉 개발한 것처럼 log를 만드는 것입니다. 이는 `one-hot` branch를 만든 이유가 단순히 `file-fragment-generator` branch의 파일들이 꼬이는 것을 원하지 않았다는 이유밖에 없기 때문입니다. 이 경우 rebase를 사용해야 합니다.

5. 먼저, `one-hot` branch를 `file-fragment-generator`의 최신 commit으로 rebase합니다. 이를 통해 마치 `one-hot` branch가 file-fragment-generator의 최신 commit에서 분기한 것처럼 보이도록 만듭니다.
    ```bash
    $ git checkout one-hot
    $ git rebase file-fragment-generator
    ```

6. 이제, `file-fragment-generator` branch는 `one-hot` branch의 변경 사항을 합칩니다. 비록 같은 merge 명령어를 사용해도, git는 rebase에 의해 이 개발이 한 줄로 이루어졌다고 생각하므로 새로운 merge commit을 만들지 않습니다.
    ```bash
    $ git checkout file-fragment-generator
    $ git merge one-hot
    ```

7. 이제, 개발이 완료되었으므로 필요없어진 `one-hot` branch를 제거합니다.
    ```bash
    $ git checkout file-fragment-generator
    $ git branch --delete one-hot
    ```

8. 지금까지의 rebase 과정으로, 비록 바버는 `one-hot` branch를 사용했지만, 기록은 마치 `file-fragment-generator`라는 하나의 branch에서 지속적으로 개발이 진행된 것처럼 수정되었습니다. 마지막으로, 바버는 `file-fragment-generator` branch를 푸시한 후, 컁님께 pull request를 보냅니다.
    ```bash
    $ git checkout file-fragment-generator
    $ git push origin file-fragment-generator
    ```
    * 바버: Pull request
    * 컁님: **Merge**

## branch 관리 방법 유의사항
제가 지금 밤에 글을 쓰고 있고, 저도 git를 잘 쓰지 못해 말이 이상하거나, 이해가 되지 않도록 서술된 부분이 많습니다. 혹시 이해되지 않는 부분이 있다면 바로 말씀해주시면 감사하겠습니다. branch를 위처럼 관리하는 것이 개발 기록을 남기거나, 프로젝트를 안전하게 관리하는 데에 큰 도움이 될 것 같습니다. 감사합니다.
