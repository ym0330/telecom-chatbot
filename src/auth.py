from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from database import DatabaseHandler
import bcrypt

# Security configuration
SECRET_KEY = "your-secret-key-here"  # In production, use environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
db = DatabaseHandler()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.get_user_by_username(username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(current_user = Depends(get_current_user)):
    if not current_user.get("is_active", True):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    """Register a new user"""
    try:
        # Create user with initial data
        success = db.create_user(username, email, password)
        if success:
            return True, "User registered successfully"
        return False, "Username or email already exists"
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return False, f"Error registering user: {str(e)}"

def login_user(username: str, password: str) -> tuple[bool, str, dict]:
    """Login user and return token"""
    try:
        success, message, user = db.verify_user(username, password)
        if not success:
            return False, message, None
        
        # Create access token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": username}, expires_delta=access_token_expires
        )
        
        # Get user's telecom data
        user_data = db.get_user_data(user["_id"])
        
        return True, "Login successful", {
            "access_token": access_token,
            "token_type": "bearer",
            "user": user,
            "user_data": user_data
        }
    except Exception as e:
        print(f"Login error: {str(e)}")
        return False, f"Error during login: {str(e)}", None

def get_user_profile(username: str) -> Optional[dict]:
    """Get user profile"""
    try:
        user = db.get_user_by_username(username)
        if not user:
            return None
            
        # Get user's telecom data
        user_data = db.get_user_data(user["_id"])
        
        # Combine user and user_data
        profile = {
            "username": user["username"],
            "email": user["email"],
            "created_at": user["created_at"],
            "last_login": user.get("last_login"),
            **user_data
        }
        return profile
    except Exception as e:
        print(f"Error getting user profile: {str(e)}")
        return None

def update_user_profile(username: str, update_data: dict) -> tuple[bool, str]:
    """Update user profile"""
    try:
        # Get user to get user_id
        user = db.get_user_by_username(username)
        if not user:
            return False, "User not found"
            
        # Separate auth data and telecom data
        auth_data = {k: v for k, v in update_data.items() 
                    if k in ["username", "email"]}
        telecom_data = {k: v for k, v in update_data.items() 
                       if k not in ["username", "email"]}
        
        # Update auth data if present
        if auth_data:
            success, message = db.update_user(username, auth_data)
            if not success:
                return False, message
        
        # Update telecom data if present
        if telecom_data:
            success = db.update_user_data(str(user["_id"]), telecom_data)
            if not success:
                return False, "Failed to update telecom data"
        
        return True, "Profile updated successfully"
    except Exception as e:
        return False, f"Error updating profile: {str(e)}"

def change_password(username: str, current_password: str, new_password: str) -> tuple[bool, str]:
    """Change user password"""
    try:
        success, message = db.change_password(username, current_password, new_password)
        return success, message
    except Exception as e:
        return False, f"Error changing password: {str(e)}" 