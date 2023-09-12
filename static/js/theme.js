let theme = "";
if (!localStorage.getItem("theme")) {
  const prefersDarkMode = window.matchMedia("(prefers-color-scheme: dark)");
  const prefersLightMode = window.matchMedia("(prefers-color-scheme: light)");

  if (prefersDarkMode.matches) {
    theme = "dark";
  } else {
    theme = "light";
  }
} else {
  theme = localStorage.getItem("theme");
}

console.log(theme);
const elementToBeChanged = [
  "chat",
  "share",
  "save",
  "account",
  "like",
  "notification",
  "close",
  "sun",
  "comment_icon",
  "menu",
  "logout",
  "settings",
  "upload",
  "activity",
];
const changeTheme = () => {
  if (theme == "light") {
    theme = "dark";
    document.body.style.backgroundColor = "black";
    comment_paragraph = document.querySelectorAll(".comment-paragraph");
    comment_paragraph.forEach((element) => {
      element.style.backgroundColor = "#00000";
      element.style.color = "#ffffff";
    });

    document.body.style.color = "#ffffff";
    elements = document.querySelectorAll(".bg-white");

    elements.forEach(function (element) {
      element.classList.remove("bg-white");
      element.classList.add("dark"); // Add class for changed style
    });

    elementToBeChanged.forEach(function (single_element) {
      active_element = document.querySelectorAll("." + single_element);

      if (single_element == "sun") {
        active_element.forEach((element) => {
          element.src = "/static/assets/dark/moon.svg";
        });
      } else if (single_element == "comment_icon") {
        active_element.forEach((element) => {
          element.src = "/static/assets/dark/comment.svg";
        });
      } else {
        active_element.forEach((element) => {
          element.src = "/static/assets/dark/" + single_element + ".svg";
        });
      }
    });

    localStorage.setItem("theme", "dark");
  } else if (theme == "dark") {
    theme = "light";
    document.body.style.color = "#000000";
    comment_paragraph = document.querySelectorAll(".comment-paragraph");
    comment_paragraph.forEach((element) => {
      element.style.backgroundColor = "#f5f5f5";
      element.style.color = "#000000";
    });
    document.body.style.backgroundColor = "rgb(230, 230, 230)";
    elements = document.querySelectorAll(".dark");

    elementToBeChanged.forEach(function (single_element) {
      active_element = document.querySelectorAll("." + single_element);

      if (single_element == "sun") {
        active_element.forEach((element) => {
          element.src = "/static/assets/light/sun.svg";
        });
      } else if (single_element == "comment_icon") {
        active_element.forEach((element) => {
          console.log(element);
          element.src = "/static/assets/light/comment.svg";
        });
      } else {
        active_element.forEach((element) => {
          element.src = "/static/assets/light/" + single_element + ".svg";
        });
      }
    });
    elements.forEach(function (element) {
      element.classList.remove("dark");
      element.classList.add("bg-white");
    });
    localStorage.setItem("theme", "light");
  }
};
const loadTheme = (theme) => {
  if (theme == "dark") {
    document.body.style.backgroundColor = "black";
    document.body.style.color = "#ffffff";
    elements = document.querySelectorAll(".bg-white");
    message_cont = document.querySelectorAll("bg-gray");
    message_cont.forEach((element) => {
      element.style.backgroundColor = "#000000";
    });
    comment_paragraph = document.querySelectorAll(".comment-paragraph");
    comment_paragraph.forEach((element) => {
      element.style.backgroundColor = "#000000";
      element.style.color = "#000000";
    });
    elements.forEach(function (element) {
      element.classList.remove("bg-white");
      element.classList.add("dark"); // Add class for changed style
    });

    elementToBeChanged.forEach(function (single_element) {
      active_element = document.querySelectorAll("." + single_element);

      if (single_element == "sun") {
        active_element.forEach((element) => {
          element.src = "/static/assets/dark/moon.svg";
        });
      } else if (single_element == "comment_icon") {
        active_element.forEach((element) => {
          element.src = "/static/assets/dark/comment.svg";
        });
      } else {
        active_element.forEach((element) => {
          element.src = "/static/assets/dark/" + single_element + ".svg";
        });
      }
    });
  } else if (theme == "light") {
    comment_paragraph = document.querySelectorAll(".comment-paragraph");
    comment_paragraph.forEach((element) => {
      element.style.backgroundColor = "#000000";
      element.style.color = "#ffffff";
    });
    document.body.style.color = "#000000";

    document.body.style.backgroundColor = "rgb(230, 230, 230)";
    elements = document.querySelectorAll(".dark");
    message_cont = document.querySelectorAll("bg-gray");
    message_cont.forEach((element) => {
      element.style.backgroundColor = "#f5f5f5";
    });
    elementToBeChanged.forEach(function (single_element) {
      active_element = document.querySelectorAll("." + single_element);

      if (single_element == "sun") {
        active_element.forEach((element) => {
          element.src = "/static/assets/light/sun.svg";
        });
      } else if (single_element == "comment_icon") {
        active_element.forEach((element) => {
          console.log(element);
          element.src = "/static/assets/light/comment.svg";
        });
      } else {
        active_element.forEach((element) => {
          element.src = "/static/assets/light/" + single_element + ".svg";
        });
      }
    });
    elements.forEach(function (element) {
      element.classList.remove("dark");
      element.classList.add("bg-white");
    });
    localStorage.setItem("theme", "light");
  }
};

document.addEventListener("DOMContentLoaded", () => {
  loadTheme(theme);
});
