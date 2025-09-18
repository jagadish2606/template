from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_filter import FilterDepends
from sqlmodel import Session
from fastapi.encoders import jsonable_encoder
from fastapi_versioning import version
from starlette.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT 
from core.database.db import get_db
from core.utils.pagination import PaginatedParams
from core.utils.pagination.schemas import PaginatedResponse
from repos.employee_repo import employee_create, employee_edit, get_employees_list
from schemas.core import ResponseModel
from schemas.employee import CreateEmployee, EditEmployee, EmployeeFilter, EmployeeList

router = APIRouter()

@router.get("/list", status_code=200, tags=["Employee"],
            description="All employee paginated list", response_model=PaginatedResponse[EmployeeList])
@version(1)
async def employee_all(db: Session = Depends(get_db),
                       params: PaginatedParams = Depends(),
                       employee_filter: EmployeeFilter = FilterDepends(EmployeeFilter)):
     return await get_employees_list(db, params.page, params.per_page, employee_filter)
    # if emp_obj:
    #     response = ResponseModel(data=emp_obj)
    #     return JSONResponse(jsonable_encoder(response), status_code=HTTP_200_OK)
    
    # response = ResponseModel(status=401, message='Users not found')
    # return JSONResponse(jsonable_encoder(response), status_code=HTTP_404_NOT_FOUND) 
    
    
    
@router.post("/add", status_code=200, tags=["Employee"],
             description="Employee add API", response_model=ResponseModel)
@version(1)
async def add_employee(data: CreateEmployee, db: Session = Depends(get_db)):
    emp_obj = await employee_create(data, db)
    if emp_obj:
        if emp_obj == 1:
            response = ResponseModel(status=409, message='Employee alreay exist')
            return JSONResponse(jsonable_encoder(response), status_code=HTTP_409_CONFLICT) 
            
        response = ResponseModel(data=emp_obj)
        return JSONResponse(jsonable_encoder(response), status_code=HTTP_200_OK)
    
    response = ResponseModel(status=401, message='Users not found')
    return JSONResponse(jsonable_encoder(response), status_code=HTTP_404_NOT_FOUND) 




@router.put("/edit", status_code=200, tags=["Employee"],
             description="Employee edit API", response_model=ResponseModel)
@version(1)
async def edit_employee(data: EditEmployee, db: Session = Depends(get_db)):
    emp_obj = await employee_edit(data, db)
    if emp_obj:
        if emp_obj == 1:
            response = ResponseModel(status=409, message='Employee does not exist')
            return JSONResponse(jsonable_encoder(response), status_code=HTTP_409_CONFLICT)   
        response = ResponseModel(data=emp_obj)
        return JSONResponse(jsonable_encoder(response), status_code=HTTP_200_OK)
    
    response = ResponseModel(status=401, message='Users not found')
    return JSONResponse(jsonable_encoder(response), status_code=HTTP_404_NOT_FOUND) 

