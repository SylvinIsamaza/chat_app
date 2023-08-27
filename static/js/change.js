function showModal() {
  document.getElementById("model").style.display = "flex";
}
function showShareModal(post_id) {
  document.getElementById("share_container").style.display = "flex";
  document.getElementById('share_container').setAttribute('data-post-id',post_id)
}

function closeShareModal() {
  document.getElementById("share_container").style.display = "none";
}

function showUploadModal() {
  console.log("uploading model");
  openModal = true;
  document.getElementById("upload__model").style.display = "flex";
}

function handleCloseUpload() {
  document.getElementById("upload__model").style.display = "none";
}

function handleClose() {
  document.getElementById("model").style.display = "none";
}

async function handleUpload(event) {
  const image_url = await converToBase64(event.target.files[0]);
  profile = document.getElementById("profile-image");
  profile.src = image_url;
  profile.classList.remove("upload__container");
  document
    .getElementById("profile-image")
    .classList.add("upload__container-image");

  document.getElementById("upload_container").style.padding = "0px";
  document.getElementById("upload_container").style.background = "transparent";
}

function handleEmailChange(e) {
  email = e.target.value;
}

function handleInputChange(data) {}
function handleSubmit(event) {
  event.preventDefault();
  document.getElementById("message").value = "";
}
async function converToBase64(file) {
  return new Promise((resolve, reject) => {
    const fileReader = new FileReader();
    fileReader.readAsDataURL(file);
    fileReader.onload = () => {
      resolve(fileReader.result);
    };
    fileReader.onerror = (error) => {
      reject(error);
    };
  });
}
comment = document.getElementById("comment").insertBefore();
