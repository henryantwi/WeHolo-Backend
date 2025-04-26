from typing import Any, Dict, List
import os
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Form
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.product import Product
from app.schemas.product import (
    Product as ProductSchema,
    ProductCreate,
    ProductUpdate,
)

router = APIRouter()

@router.get("/", response_model=List[ProductSchema])
def get_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Get all products for the current user.
    """
    products = (
        db.query(Product)
        .filter(Product.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .all()
    )
    return products

@router.post("/", response_model=ProductSchema)
def create_product(
    *,
    db: Session = Depends(get_db),
    product_in: ProductCreate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Create a new product.
    """
    product = Product(
        name=product_in.name,
        description=product_in.description,
        image_url=product_in.image_url,
        price=product_in.price,
        user_id=current_user.id,
    )
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product

@router.get("/{product_id}", response_model=ProductSchema)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Get a specific product by ID.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Check if user owns this product
    if product.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to access this product",
        )
    
    return product

@router.put("/{product_id}", response_model=ProductSchema)
def update_product(
    *,
    product_id: int,
    db: Session = Depends(get_db),
    product_in: ProductUpdate,
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Update a product.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Check if user owns this product
    if product.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to modify this product",
        )
    
    # Update product attributes
    if product_in.name is not None:
        product.name = product_in.name
    
    if product_in.description is not None:
        product.description = product_in.description
    
    if product_in.image_url is not None:
        product.image_url = product_in.image_url
    
    if product_in.price is not None:
        product.price = product_in.price
    
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return product

@router.delete("/{product_id}", response_model=Dict[str, Any])
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Delete a product.
    """
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Check if user owns this product
    if product.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions to delete this product",
        )
    
    db.delete(product)
    db.commit()
    
    return {"success": True, "message": "Product deleted successfully"}

@router.post("/upload-image", response_model=Dict[str, Any])
async def upload_product_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
) -> Any:
    """
    Upload a product image.
    In a real implementation, this would save the file to a storage service.
    """
    # In a real implementation, we would:
    # 1. Validate the file (type, size, etc.)
    # 2. Save the file to a storage service (e.g., AWS S3)
    # 3. Return the URL of the saved file
    
    # For this example, we'll just return a mock URL
    file_extension = os.path.splitext(file.filename)[1] if file.filename else ".jpg"
    mock_url = f"https://example.com/products/{current_user.id}_{file.filename}"
    
    return {
        "success": True,
        "message": "Image uploaded successfully",
        "image_url": mock_url,
    }