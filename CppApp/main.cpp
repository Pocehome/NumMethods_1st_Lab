//#include "TestTask.h"
//#include "FirstTask.h"
//#include "SecondTask.h"
//#include <iostream>
//#include <locale>
//
//
//int main()
//{
//	setlocale(LC_ALL, "Russian");
//	double A{};
//	double B{};
//	double STEP{};
//	double E_BORDER{};
//	double E_ERROR{};
//	int MAX_STEPS{};
//	double START_POINT_FOR_U{};
//
//	std::cout << "0 - �������� ������   1 - ������ ������  2 - ������ ������ " << std::endl;
//	int task;
//	std::cin >> task;
//	
//	int option;
//	
//	std::cout << "1 - ��� ���     2 - � ���" << std::endl << std::endl;
//	std::cout << "�������� ������� �������: ";
//	std::cin >> option;
//	std::cout << std::endl;
//
//	double a;
//	if (task == 2) {
//		
//		std::cout << "������� �������� �: " << std::endl;
//		std::cin >> a;
//	}
//
//	std::cout << "������� ����� ������� �������������� �: " << std::endl;
//	std::cin >> A;
//
//	std::cout << "������� ������ ������� �������������� B: " << std::endl;
//	std::cin >> B;
//
//	std::cout << "������� ��� �������������� STEP: " << std::endl;
//	std::cin >> STEP;
//
//	std::cout << "������� E ��� ������ �� E_ERROR: " << std::endl;
//	std::cin >> E_ERROR;
//
//	std::cout << "������� E-��������� E_BORDER: " << std::endl;
//	std::cin >> E_BORDER;
//
//	std::cout << "������� ������������ ����� ����� MAX_STEPS: " << std::endl;
//	std::cin >> MAX_STEPS;
//
//	std::cout << "������� ��������� ������� U(A): " << std::endl;
//	std::cin >> START_POINT_FOR_U;
//
//	if (task == 0) {
//		TestTask Solution(A, B, STEP, E_ERROR, E_BORDER, MAX_STEPS, START_POINT_FOR_U);
//		
//		if (option == 1) {
//
//			Solution.Solve_Without_Error_Control();
//		}
//		if (option == 2) {
//			Solution.Solve_With_Error_Control();
//		}
//
//		Solution.Write_To_File();
//		Solution.PrintTable();
//		Solution.PrintReference();
//	}
//
//	if (task == 1) {
//		FirstTask Solution1(A, B, STEP, E_ERROR, E_BORDER, MAX_STEPS, START_POINT_FOR_U);
//		if (option == 1) {
//
//			Solution1.Solve_Without_Error_Control();
//		}
//		if (option == 2) {
//			Solution1.Solve_With_Error_Control();
//		}
//
//		Solution1.Write_To_File();
//		Solution1.PrintTable();
//		Solution1.PrintReference();
//	}
//
//	if (task == 2) {
//		SecondTask Solution2(A, B, STEP, E_ERROR, E_BORDER, MAX_STEPS, START_POINT_FOR_U);
//		Solution2.set_alpha(a);
//		if (option == 1) {
//
//			Solution2.Solve_Without_Error_Control();
//		}
//		if (option == 2) {
//			Solution2.Solve_With_Error_Control();
//		}
//
//		Solution2.Write_To_File();
//		Solution2.PrintTable();
//		Solution2.PrintReference();
//	}
//
//}