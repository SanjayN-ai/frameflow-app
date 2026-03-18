const input = document.getElementById("upload");
const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

let images = [];

input.addEventListener("change", async (e) => {
  const files = e.target.files;

  if (files.length < 3) {
    alert("Upload at least 3 images");
    return;
  }

  images = [];

  for (let file of files) {
    let img = new Image();
    img.src = URL.createObjectURL(file);

    await new Promise(res => img.onload = res);
    images.push(img);
  }
});

function generate() {
  const phi = 1.618;

  canvas.width = 1000;
  canvas.height = 600;

  let mainWidth = canvas.width / phi;
  let sideWidth = canvas.width - mainWidth;

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  ctx.drawImage(images[0], 0, 0, mainWidth, canvas.height);

  let subHeight = canvas.height / phi;

  ctx.drawImage(images[1], mainWidth, 0, sideWidth, subHeight);
  ctx.drawImage(images[2], mainWidth, subHeight, sideWidth, canvas.height - subHeight);
}

function download() {
  const link = document.createElement("a");
  link.download = "frameflow.png";
  link.href = canvas.toDataURL();
  link.click();
}