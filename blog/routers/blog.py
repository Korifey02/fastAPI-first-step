from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from ..schemas import *
from .. import models
from ..database import *

router = APIRouter(
    prefix="/blog",
    tags=['blogs']

)

@router.get('/', response_model= List[ShowBlog])
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def destroy(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Blog with id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'

@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
        detail =f"Blog with id {id} not found")
    blog.update(request.dict())
    db.commit()
    return 'updated'

@router.get('/{id}', status_code=200, response_model=ShowBlog)
def show(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} is not available")
        # THE   STRIND BEHIND IS THE SMAE TO TWO ONES FATHER

        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"Blog withe the id {id} is not available"}
    return blog