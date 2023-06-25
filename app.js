    
    
AWS.config.region = 'us-east-1'; // Reemplaza 'REGION' con tu región de AWS
AWS.config.credentials = new AWS.Credentials('ASIA3U745VZBAWKT53NY', 'nwNkXSDU8XZxn0M9UzuNllm9zTZZcRBnirXH6lrL'); // Reemplaza 'ACCESS_KEY' y 'SECRET_KEY' con tus propias credenciales de AWS

function subirArchivo() {
  var archivo = document.getElementById("archivo").files[0];
  var nombreArchivo = archivo.name;
  var bucketNombre = 'image-bucket-pro'; // Reemplaza 'NOMBRE_BUCKET' con el nombre de tu bucket en Amazon S3
  var rutaEspecifica = 'usersFaces/'; // Ruta específica dentro del bucket

  var bucket = new AWS.S3({
    params: { Bucket: bucketNombre }
  });

  var params = {
    Key: rutaEspecifica + nombreArchivo,
    Body: archivo,
    ACL: 'public-read' // Opcional: Cambia esto según tus necesidades de permisos
  };

  bucket.upload(params, function (err, data) {
    if (err) {
      console.log("Error al subir el archivo: ", err);
    } else {
      console.log("Archivo cargado exitosamente. URL pública: ", data.Location);
    }
  });
}
