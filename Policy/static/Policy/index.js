DOB_inputBox = document.querySelector(".form-control.inputDOB");
effectiveDate_inputBox = document.querySelector(".form-control.inputEffectiveDate");
DOB_Agent_inputBox = document.querySelector(".form-control.inputDOB-agent");

effectiveDate_calender = flatpickr(".fa-calendar.effective-date", {
  dateFormat: "d/m/Y",
  onChange: function (selectedDates, dateStr, instance) {
    effectiveDate_inputBox.value = dateStr;
  },
});

DOB_calender = flatpickr(".fa-calendar.DOB", {
  dateFormat: "d/m/Y",
  onChange: function (selectedDates, dateStr, instance) {
    DOB_inputBox.value = dateStr;
  },
});

DOB_agent_calender = flatpickr(".fa-calendar.DOB-agent", {
  dateFormat: "d/m/Y",
  onChange: function (selectedDates, dateStr, instance) {
    DOB_Agent_inputBox.value = dateStr;
  },
});

// let selectedDate = selectedDates[0];
// let selectedDateWithCurrentTime = new Date(
//   selectedDate.setHours(currentDate.getHours(), currentDate.getMinutes(), currentDate.getSeconds())
// );
// console.log(instance);
// console.log(selectedDates);
// // console.log(selectedDateWithCurrentTime.toISOString());
// console.log(JSON.stringify(selectedDateWithCurrentTime).slice(1, 11));
// console.log(dateStr);
