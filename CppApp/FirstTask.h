#pragma once
#include "TestTask.h"

class FirstTask:public TestTask
{

protected:
    virtual double f(const double& _X, const double& _V) override;

public:
    FirstTask(const double& _A, const double& _B, const double& _STEP, const double& _E_ERROR,
              const double& _E_BORDER, const int& _MAX_STEPS, const double& _START_POINT)
    : TestTask(_A, _B, _STEP, _E_ERROR, _E_BORDER, _MAX_STEPS, _START_POINT) {};

    void Solve_With_Error_Control() override;
    void Solve_Without_Error_Control() override;

    // ������� ��� �������� � main , � �������� ��������, ��� ����� �� �����
    void virtual PrintTable() override;     //����� �������� ������� �� �������, ���� ����� ������ ������ �������, ����� �� �����������
    void virtual Write_To_File() override;  //������ X,Vi,Ui � ����
    void virtual PrintReference() override; //����� �������� �������
};

