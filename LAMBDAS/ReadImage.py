
import json
import boto3
#from decimal import Decimal

def get_emotions(response):
    if 'FaceDetails' in response and len(response['FaceDetails']) > 0:
        result = response['FaceDetails'][0]['Emotions'][0]
        result["Confidence"] = str(result["Confidence"])
        return result 
    else:
        raise ValueError("No se detectaron caras en la imagen")

def recognize_celebrities(image_data):
    rekognition = boto3.client('rekognition')
    response = rekognition.recognize_celebrities(
        Image={'Bytes': image_data}
    )
    return response

def detect_faces(image_data):
    rekognition = boto3.client('rekognition')
    response = rekognition.detect_faces(
        Image={'Bytes': image_data},
        Attributes=['ALL']
    )
    return response

def lambda_handler(event, context):
    # Obtener nombre de archivo y nombre de bucket
    file_name = event['Records'][0]['s3']['object']['key']
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    

    # Obtener imagen desde S3
    s3 = boto3.client('s3')
    print(bucket_name, file_name)
    response = s3.get_object(Bucket=bucket_name, Key=file_name)
    print(response)
    image = response['Body']
    print(image)
    image_data = image.read()
    print(image_data)
    
    
    # Reconocimiento de celebridades
    celebrities_info = []
    response_celebrities = recognize_celebrities(image_data)
    if 'CelebrityFaces' in response_celebrities and len(response_celebrities['CelebrityFaces']) > 0:
        celebrities = response_celebrities['CelebrityFaces']
        for celebrity in celebrities:
            name = celebrity['Name']
            confidence = str(celebrity['MatchConfidence'])
            celebrities_info.append({'name': name, 'similarity': confidence})
            print(f"Celebridad: {name} (Confianza: {confidence}%)")
    else:
        print("No se encontraron caras de celebridades en la imagen.")

    
    # Detección de emociones
    user_emotion = {}
    print("Detección de emociones")
    response_faces = detect_faces(image_data)
    print(response_faces)

    try:
        print("try")
        user_emotion = get_emotions(response_faces)
        tenant_id = user_emotion['Type']
        if tenant_id not in ["HAPPY", "SAD", "SURPRISED"]:
            tenant_id = "OTHER"
    except ValueError as e:
        print("except")
        print(str(e))
        tenant_id = "NONE"
    
    print(user_emotion)
    print(tenant_id)
        
        
    #Resultado
    result = {
        'tenant_id': tenant_id,
        'image_id': file_name,
        'image_data': {
            'celebrities_info': celebrities_info,
            'user_emotion': user_emotion
        }
    }
    print(result)
    
    
    # Publicar en SNS
    sns_client = boto3.client('sns')
    response_sns = sns_client.publish(
        TopicArn='arn:aws:sns:us-east-1:801004957250:NewImage',
        Subject='ThemeNewImage',
        Message=json.dumps(result),
        MessageAttributes={
            'tenant_id': {'DataType': 'String', 'StringValue': tenant_id}
        }
    )
    print(response_sns)


    # Salida (json)
    return {
        'statusCode': 200,
        'body': response_sns
    }
