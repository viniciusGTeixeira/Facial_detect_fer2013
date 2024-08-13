import cv2
import numpy as np
from tensorflow.keras.models import load_model

# Carregar o modelo treinado
model = load_model('emotion_detection_model.h5')

# Dicionário de emoções
emotion_dict = {0: 'Raiva', 1: 'Nojo', 2: 'Medo', 3: 'Feliz', 4: 'Triste', 5: 'Surpreso', 6: 'Neutro'}

# Iniciar a captura de vídeo
cap = cv2.VideoCapture(0)

while True:
    # Capturar frame por frame
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Converter para escala de cinza
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detectar rostos no frame
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.3, minNeighbors=5)
    
    for (x, y, w, h) in faces:
        roi_gray = gray_frame[y:y + h, x:x + w]
        roi_gray = cv2.resize(roi_gray, (48, 48))
        roi_gray = roi_gray.astype('float32') / 255
        roi_gray = np.expand_dims(roi_gray, axis=0)
        roi_gray = np.expand_dims(roi_gray, axis=-1)
        
        prediction = model.predict(roi_gray)
        max_index = int(np.argmax(prediction))
        predicted_emotion = emotion_dict[max_index]
        
        # Desenhar um retângulo ao redor do rosto e escrever a emoção prevista
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.putText(frame, predicted_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    # Mostrar o frame com a emoção prevista
    cv2.imshow('Detecção de Emoção', frame)
    
    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura e fechar as janelas
cap.release()
cv2.destroyAllWindows()
