$(document).ready(function () {
  const ctx = document.getElementById("myChart");
  const myChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["ROIA", "ROIB", "ROIC", "ROID"],
      datasets: [
        {
          label: "Person in Area",
          borderWidth: 2,
          borderColor: ["rgba(255, 99, 132, 1)"],
          backgroundColor: [
            "rgba(255, 99, 132, 0.2)",
            "rgba(255, 159, 64, 0.2)",
            "rgba(75, 192, 192, 0.2)",
            "rgba(54, 162, 235, 0.2)",
          ],
        },
      ],
    },
    options: {
      indexAxis: "y",
      scales: {
        x: {
          beginAtZero: true,
        },
      },
    },
  });

  function addData(dataA, dataB, dataC, dataD) {
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.push(dataA);
      dataset.data.push(dataB);
      dataset.data.push(dataC);
      dataset.data.push(dataC);
      console.log(dataset.data);
    });
    myChart.update();
  }

  function removeFirstData() {
    myChart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
      dataset.data.shift();
      dataset.data.shift();
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 4;
  //connect to the socket server.
  var socket = io.connect();

  //receive details from server
  socket.on("updateROI", function (msg) {
    removeFirstData();
    addData(msg.dataA, msg.dataB, msg.dataC, msg.dataD);
  });


  socket.on("sendMsg", function (msg) {
    let wrapper = document.getElementById("alert-frame");
    let myHTML = '';
    for (const property in msg.msg) {
      console.log(`${property}: ${msg.msg[property]}`);
      myHTML +=
        '<div id="alert"><span>' +
        msg.msg[property] +
        '</span> <span class="closebtn" onclick="this.parentElement.style.display='+"'none'"+';">&times;</span></div>';
      wrapper.innerHTML = myHTML;
    }
  });
});
