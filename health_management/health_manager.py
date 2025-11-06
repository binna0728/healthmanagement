import pymysql
from pymysql.cursors import DictCursor


def get_db_connection() -> pymysql.Connection:
    """MySQL 연결 객체 생성"""
    try:
        return pymysql.connect(
            host="localhost",
            port=3307,
            user="root",
            password="1234",
            database="health_db",
            cursorclass=DictCursor,
        )
    except Exception as e:
        print(f"데이터베이스 연결 실패: {e}")
        exit(1)


def add_record(cursor: DictCursor):
    """건강 기록 추가"""
    try:
        height = int(input("키(cm): "))
        weight = int(input("몸무게(kg): "))
        memo = input("메모(선택사항): ")

        sql = """
        INSERT INTO health_records (height, weight, memo)
        VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (height, weight, memo if memo else None))
        print("건강 기록이 추가되었습니다.")
    except ValueError:
        print("키와 몸무게는 숫자로 입력해주세요.")
    except Exception as e:
        print(f"기록 추가 중 오류 발생: {e}")


def get_records(cursor: DictCursor):
    """건강 기록 조회"""
    try:
        cursor.execute(
            """
            SELECT id, height, weight, memo, created_at
              FROM health_records
             ORDER BY created_at DESC
            """
        )
        records = cursor.fetchall()

        if not records:
            print("\n등록된 건강 기록이 없습니다.")
            return

        print("\n=== 건강 기록 목록 ===")
        for record in records:
            record_id = record["id"]
            height = record["height"]
            weight = record["weight"]
            memo = record["memo"]
            created_at = record["created_at"]
            memo_text = memo if memo else "-"
            # BMI 계산
            bmi = weight / ((height / 100) ** 2)
            bmi_category = ""
            if bmi < 18.5:
                bmi_category = "저체중"
            elif 18.5 <= bmi < 24.9:
                bmi_category = "정상체중"   
            else:
                bmi_category = "과체중"

            print(
                f"[{record_id}] 키: {height}cm | 몸무게: {weight}kg | 메모: {memo_text} | 생성일: {created_at} | BMI: {bmi:.2f} | BMI 분류: {bmi_category}"
            )
    except Exception as e:
        print(f"기록 조회 중 오류 발생: {e}")


def update_record(cursor: DictCursor):
    """건강 기록 수정"""
    try:
        record_id = int(input("수정할 기록 ID: "))
        cursor.execute(
            "SELECT height, weight, memo FROM health_records WHERE id = %s",
            (record_id,),
        )
        current = cursor.fetchone()

        if not current:
            print("해당 ID의 기록이 없습니다.")
            return

        current_height = current["height"]
        current_weight = current["weight"]
        current_memo = current["memo"]
        current_bmi = current["bmi"]
        current_bmi_category = current["bmi_category"]
        print(
            f"현재 값 - 키: {current_height}cm, 몸무게: {current_weight}kg, 메모: {current_memo or '-'}, BMI: {current_bmi:.2f}, BMI 분류: {current_bmi_category}"
        )

        new_height = input("새 키(cm) (Enter 유지): ").strip()
        new_weight = input("새 몸무게(kg) (Enter 유지): ").strip()
        new_memo = input("새 메모(Enter 유지): ")
        new_bmi = None
        new_bmi_category = None 
        updates = []
        params = []

        if new_height:
            updates.append("height = %s")
            params.append(int(new_height))
        if new_weight:
            updates.append("weight = %s")
            params.append(int(new_weight))
        if new_memo.strip() != "":
            updates.append("memo = %s")
            params.append(new_memo if new_memo else None)
        if new_bmi is not None:
            updates.append("bmi = %s")
            params.append(new_bmi)
        if new_bmi_category is not None:    
            updates.append("bmi_category = %s")
            params.append(new_bmi_category)

        if not updates:
            print("변경 사항이 없습니다.")
            return

        params.append(record_id)
        sql = f"UPDATE health_records SET {', '.join(updates)} WHERE id = %s"
        cursor.execute(sql, params)
        print("건강 기록이 수정되었습니다.")
    except ValueError:
        print("ID, 키, 몸무게에는 숫자를 입력해주세요.")
    except Exception as e:
        print(f"기록 수정 중 오류 발생: {e}")


def delete_record(cursor: DictCursor):
    """건강 기록 삭제"""
    try:
        record_id = int(input("삭제할 기록 ID: "))
        cursor.execute(
            "SELECT COUNT(*) AS record_count FROM health_records WHERE id = %s",
            (record_id,),
        )
        exists = cursor.fetchone()
        count = exists["record_count"] if exists else 0

        if count == 0:
            print("해당 ID의 기록이 없습니다.")
            return

        confirm = input("정말 삭제하시겠습니까? (y/N): ").strip().lower()
        if confirm != "y":
            print("삭제를 취소했습니다.")
            return

        cursor.execute("DELETE FROM health_records WHERE id = %s", (record_id,))
        print("건강 기록이 삭제되었습니다.")
    except ValueError:
        print("ID에는 숫자를 입력해주세요.")
    except Exception as e:
        print(f"기록 삭제 중 오류 발생: {e}")


def show_menu() -> str:
    """메뉴 표시"""
    print("\n=== 건강 관리 프로그램 ===")
    print("1. 건강 기록 추가")
    print("2. 건강 기록 조회")
    print("3. 건강 기록 수정")
    print("4. 건강 기록 삭제")
    print("5. 종료")
    return get_user_choice()


def get_user_choice() -> str:
    """사용자 선택 입력"""
    return input("\n선택: ")


def main():
    """메인 루프"""
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        while True:
            choice = show_menu()

            if choice == "1":
                add_record(cursor)
                conn.commit()
            elif choice == "2":
                get_records(cursor)
            elif choice == "3":
                update_record(cursor)
                conn.commit()
            elif choice == "4":
                delete_record(cursor)
                conn.commit()
            elif choice == "5":
                print("프로그램을 종료합니다.")
                break
            else:
                print("올바른 메뉴를 선택해주세요.")
    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    main()
