const nav_links = document.querySelectorAll(".nav__item-link");
const sub_links = document.querySelectorAll(".sub_link");

function collapse_nav(head, toggler, sidenav) {
  const header = document.getElementById(head);
  const nav_toggler = document.getElementById(toggler);
  const nav = document.getElementById(sidenav);

  nav_toggler.addEventListener("click", function () {
    this.classList.toggle("fa-times");
    nav.classList.toggle("collapse");
    header.classList.toggle("collapse-header");
  });
}

collapse_nav("header", "nav-toggler", "nav");

nav_links.forEach((link) => {
  link.addEventListener("click", function () {
    nav_links.forEach((l) => {
      if (l.classList.contains("active")) {
        l.classList.remove("active");
      }
    });

    this.classList.toggle("active");
    const sub_menu = this.nextElementSibling;
    if (sub_menu) {
      sub_menu.classList.toggle("d-none");
    }
  });
});

sub_links.forEach((link) => {
  link.addEventListener("click", () => {
    sub_links.forEach((l) => l.classList.remove("active-sub-link"));
    link.classList.toggle("active-sub-link");
  });
});
const prevBtns = document.querySelectorAll(".btn-prev");
  const nextBtns = document.querySelectorAll(".btn-next");
  const progress = document.getElementById("progress");
  const formSteps = document.querySelectorAll(".form-step");
  const progressSteps = document.querySelectorAll(".progress-step");

  let formStepsNum = 0;

  nextBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      formStepsNum++;
      updateFormSteps();
      updateProgressbar();
    });
  });

  prevBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      formStepsNum--;
      updateFormSteps();
      updateProgressbar();
    });
  });

  function updateFormSteps() {
    formSteps.forEach((formStep) => {
      formStep.classList.contains("form-step-active") &&
        formStep.classList.remove("form-step-active");
    });

    formSteps[formStepsNum].classList.add("form-step-active");
  }

  function updateProgressbar() {
    progressSteps.forEach((progressStep, idx) => {
      if (idx < formStepsNum + 1) {
        progressStep.classList.add("progress-step-active");
      } else {
        progressStep.classList.remove("progress-step-active");
      }
    });

    const progressActive = document.querySelectorAll(".progress-step-active");

    progress.style.width =
      ((progressActive.length - 1) / (progressSteps.length - 1)) * 100 + "%";
  }


  
  

//   ViewRecord.addEventListener('click', (e) => {
//     if (tablecontainer.classList.contains('hidden')) {
//         // Navigate to the view route if the table is hidden
//         window.location.href = "{{ url_for('view_data') }}";
//     } else {
//         // Prevent default if the table is already visible
//         e.preventDefault();
//         formcontainer.classList.add('hidden');
//         tablecontainer.classList.remove('hidden');
//     }
// });

// AddRecord.addEventListener('click', (e) => {
//     e.preventDefault(); // Prevent default behavior to avoid refresh
//     tablecontainer.classList.add('hidden');
//     formcontainer.classList.remove('hidden');
// });

