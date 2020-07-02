from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import  User
from .models import Profile  
import face_recognition

class FaceAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None,image = None, **kwargs):
        try:
            profile = Profile.objects.get(username=username)
            if profile.user.check_password(password) and self.check_face_id(profile.picture, image) :
                return profile.user
        except Profile.DoesNotExist:
            pass
    
    def check_face_id(self, profilePicture, image) :
        
        known_image = face_recognition.load_image_file(profilePicture)
        unknown_image = face_recognition.load_image_file(image)

        known_face_locations = face_recognition.face_locations(known_image)
        unknown_face_locations = face_recognition.face_locations(unknown_image)

        known_face_embedding = face_recognition.face_encodings(known_image, known_face_locations)[0]
        unknown_face_embedding = face_recognition.face_encodings(unknown_image, unknown_face_locations)[0]

        matches = face_recognition.compare_faces([known_face_embedding], unknown_face_embedding)

        if matches[0]:
            return True
        else :
            return False

