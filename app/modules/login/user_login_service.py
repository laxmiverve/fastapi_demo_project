from sqlalchemy.orm import Session
from app.hashing.password_hash import Hash
from app.auth.jwt_handler import create_access_token, decode_jwt_token
from app.models.company_model import CompanyModel
from app.models.roles_model import Role
from app.models.user_company_model import UserCompany
from app.models.user_model import UserModel
from app.modules.company.company_service import BASE_URL
from app.schemas.user_response_schema import CompanyDetailSchema
from app.helper.email_sender import Helper


# user login
def login_user(email: str, password: str, db: Session):
    try:
        if not Helper.is_valid_email(email):
            return 1
        
        user = db.query(UserModel).filter(UserModel.email == email).first()

        if not user or not Hash.verify(user.password, password):
            return None
        
        # return the role of user
        role = db.query(Role).filter(Role.id == user.role_id).first()
        if not role:
            return None
        
        access_token = create_access_token(data={"sub": user.email})

        return {
            "name": user.name,
            "email": user.email,
            "access_token": access_token,
            "role": role.role_name
        }
    
    except Exception as e:
        print("An exception occurred:", str(e))



# get user information by access token
def userinfo_by_token(token: str, db: Session):
    try:
        if not token:
            return 1  # token was not found
        
        email = decode_jwt_token(token)
        
        if email is None:
            return None

        user = db.query(UserModel).filter(UserModel.email == email).first()
        
        if not user:
            return None

        role = db.query(Role).filter(Role.id == user.role_id).first()
        if not role:
            return None

        user_company = db.query(UserCompany).filter(UserCompany.user_id == user.id).first()
        
        company_details = None

        if user_company:
            company = db.query(CompanyModel).filter(CompanyModel.id == user_company.company_id).first()
            if company:
                company_details = CompanyDetailSchema(
                    company_id = company.id,
                    company_name = company.company_name,
                    company_email = company.company_email
                )

        profile_img_url = f"{BASE_URL}{user.profile_img}" if user.profile_img else None
        
        return {
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "role_id": user.role_id,
            "role_name": role.role_name,
            "city": user.city,
            "state": user.state,
            "country": user.country,
            "profile_img": profile_img_url,  
            "company_details": company_details
        }
    
    except Exception as e:
        print("An exception occurred:", str(e))
