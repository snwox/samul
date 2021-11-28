let carTimer = [];

(function setCarTimer() {
    if(Timer !== undefined) clearInterval(Timer);
    
    carTimer = [];

    for(let i of cars) {
        carTimer.push({
            carTimeTable: document.querySelector(`#u${i.id} > .nowTime`),
            carFeeTable: document.querySelector(`#u${i.id} > .nowPrice`),
            enterTime: i.enter_timeS
        });
    }
    
    Timer = setInterval(() => {
        for(let car of carTimer) {
            const now = new Date();
            const enter = new Date(car.enterTime);
            const time = now - enter;
    
            const day = Math.floor(time / 1000 / 60 / 60 / 24);
            const hour = Math.floor(time / 1000 / 60 / 60);
            const minute = Math.floor(time / 1000 / 60);
            const seconds = Math.floor(time / 1000);
    
            car.carTimeTable.innerHTML = `${day}일 ${hour}시 ${minute}분 ${seconds}초`;
            car.carFeeTable.inneerHTML = `${Math.floor(minute/5) * 400} 원`;
        }
    }, 1000);
})();