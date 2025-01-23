import subprocess

def add_location_to_file(filename, new_location):
    """
    주어진 파일에 새로운 위치를 추가하는 함수.
    
    :param filename: 위치가 저장된 파일 경로 (예: where.data)
    :param new_location: 추가하려는 위치 (예: '서울특별시 종로구 성균관로 25-2')
    """
    try:
        # 파일을 열고 새로운 위치를 추가
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(new_location + '\n')
        print(f"새로운 위치가 추가되었습니다: {new_location}")
    except Exception as e:
        print(f"파일을 수정하는 중 문제가 발생했습니다: {e}")

def run_script(script_name):
    """
    주어진 파이썬 스크립트를 실행하는 함수.
    
    :param script_name: 실행할 스크립트 이름 (예: geoload.py)
    """
    try:
        print(f"실행 중: {script_name}")
        subprocess.run(["python", script_name], check=True)
        print(f"{script_name} 실행 완료")
    except subprocess.CalledProcessError as e:
        print(f"{script_name} 실행 중 오류 발생: {e}")
    except FileNotFoundError:
        print(f"{script_name} 파일을 찾을 수 없습니다.")

# 실행 예시
if __name__ == "__main__":
    # where.data 파일 이름
    file_name = "where.data"
    # 추가할 위치 입력
    location_to_add = input("추가할 위치를 입력하세요 (예: 서울특별시 종로구 성균관로 25-2): ")
    # 위치 추가 함수 호출
    add_location_to_file(file_name, location_to_add)
    
    # geoload.py 실행
    run_script("geoload.py")
    
    # geodump.py 실행
    run_script("geodump.py")
