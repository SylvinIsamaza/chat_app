function handleCloseNotification(){
  document.getElementById("notification_cont").style.display = "none"
  document.getElementById("notification__model").style.display="none"
}
function showModal() {
  handleCloseNotification()
  handleCloseUpload()
  document.getElementById("model").style.display = "flex";  
  

}

function handleMessageModal() {
  element = document.getElementById("message_model");
  if (element.style.display == "none") {
    showMessageModal();
    showSearchMobile();
  } else {
    closeMessageModal();
  }
}
element = document.querySelector(".mobile_nav .search");
element.addEventListener("click", () => showSearchMobile());
function showSearchMobile() {
  console.log("clicked");
  {
    document.getElementById("search__div").style.display = "block";

    element.style.display = "none";
  }
}

function showMessageModal() {
  document.getElementById("message_model").style.display = "flex";
}
function closeMessageModal() {
  document.getElementById("message_model").style.display = "none";
}
function showShareModal(post_id) {
  document.getElementById("share_container").style.display = "flex";
  
  document
    .getElementById("post-share-id")
    .setAttribute("value", post_id);
}

function closeShareModal() {
  document.getElementById("share_container").style.display = "none";
}

function showUploadModal() {
  console.log("uploading model");
  handleCloseNotification()

  handleClose()
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

