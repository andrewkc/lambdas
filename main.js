AWS.config.update({
    credentials: new AWS.Credentials('ASIARV4UP62ZHMLQFKGO', 'PiaGvQZhMNfUi4AgddNmNzguOXJjGYw58CSlqEVL'),
    region: 'us-east-1'
});

var s3 = new AWS.S3();
var lambda = new AWS.Lambda();

document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault();

    var file = document.getElementById('imageInput').files[0];

    var reader = new FileReader();
    reader.onload = function () {
        var fileContent = reader.result.split(',')[1]; // Convertir a cadena base64
        
        var lambdaParams = {
            FunctionName: 'ReadImagesUsers',
            InvocationType: 'Event',
            Payload: JSON.stringify({ image: fileContent })
        };

        lambda.invoke(lambdaParams, function (err, data) {
            if (err) {
                console.log('Error al invocar la función Lambda: ', err);
            } else {
                console.log('Imagen enviada exitosamente al Lambda');
            }
        });
    };

    reader.readAsDataURL(file); // Leer como una cadena base64
});
