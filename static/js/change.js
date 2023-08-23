let open = false;
function showModal() {
  open = true;
  document.getElementById("model").style.display ="flex";
 

}
let openModal=false

function showUploadModal(){
console.log('uploading model')
openModal=true
document.getElementById("upload__model").style.display="flex"
}

function handleCloseUpload() {
  open = false;
  document.getElementById("upload__model").style.display = "none";


}

function handleClose() {
  open = false;
  document.getElementById("model").style.display = "none";
  

}

function handleUpload(event){
  const image_url= URL.createObjectURL(event.target.files[0])
console.log(image_url)
}

function handleEmailChange(e){
email=e.target.value

}

function handleInputChange(data){

}
function handleSubmit(event) {
  event.preventDefault()
  document.getElementById("message").value=""
}