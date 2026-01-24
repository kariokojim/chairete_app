/* ======================================================
   MEMBER CONTEXT HANDLING (CRITICAL)
   ====================================================== */

function setMemberNo(memberNo) {
  const ids = [
    'edit_member_no',
    'nok_member_no',
    'beneficiary_member_no'
  ];

  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.value = memberNo;
  });
}


/* ======================================================
   EDIT MEMBER MODAL (PRELOAD DATA)
   ====================================================== */

function editMember(member) {
  const set = (selector, value) => {
    const el = document.querySelector(selector);
    if (el) el.value = value || '';
  };

  set('#edit_member_no', member.member_no);
  set('[name="name"]', member.name);
  set('[name="phone"]', member.phone);
  set('[name="email"]', member.email);
  set('[name="id_no"]', member.id_no);
  set('[name="congregation"]', member.congregation);
  set('[name="gender"]', member.gender);
  set('[name="dob"]', member.dob);
  set('[name="joined_date"]', member.joined_date);
}


/* ======================================================
   BENEFICIARIES (DYNAMIC ROWS + % VALIDATION)
   ====================================================== */

function addBeneficiaryRow() {
  const tbody = document.getElementById('beneficiariesBody');
  if (!tbody) return;

  const row = document.createElement('tr');
  row.innerHTML = `
    <td>
      <input class="form-control" name="ben_full_name[]" required>
    </td>
    <td>
      <input class="form-control" name="ben_relationship[]">
    </td>
    <td>
      <input class="form-control" name="ben_contact[]">
    </td>
    <td>
      <input type="number" step="0.01" min="0" max="100"
             class="form-control ben-percent"
             name="ben_percentage[]"
             oninput="updateTotal()">
    </td>
    <td class="text-center">
      <button type="button" class="btn btn-sm btn-danger"
              onclick="removeBeneficiaryRow(this)">
        ✖
      </button>
    </td>
  `;

  tbody.appendChild(row);
}

function removeBeneficiaryRow(btn) {
  const row = btn.closest('tr');
  if (row) row.remove();
  updateTotal();
}

function updateTotal() {
  let total = 0;

  document.querySelectorAll('.ben-percent').forEach(el => {
    total += parseFloat(el.value) || 0;
  });

  const totalEl = document.getElementById('totalPercent');
  if (totalEl) {
    totalEl.innerText = total.toFixed(2) + '%';
    totalEl.className =
      total === 100 ? 'text-success fw-bold' : 'text-danger fw-bold';
  }
}

function validateBeneficiaries() {
  let total = 0;

  document.querySelectorAll('.ben-percent').forEach(el => {
    total += parseFloat(el.value) || 0;
  });

  if (total !== 100) {
    alert(
      'Beneficiary percentage must total exactly 100%.\n' +
      'Current total: ' + total.toFixed(2) + '%'
    );
    return false;
  }

  return true;
}
function showSection(section) {
  document.querySelectorAll('.member-section').forEach(div => {
    div.classList.add('d-none');
  });

  const target = document.getElementById('section-' + section);
  if (target) {
    target.classList.remove('d-none');
  }
}
document.getElementById('toggleOpening')?.addEventListener('change', function () {
  document.querySelectorAll('.opening-col').forEach(col => {
    col.style.display = this.checked ? '' : 'none';
  });
});

function lookupMember() {
  const memberNo = document.getElementById('memberNo').value.trim();
  const nameField = document.getElementById('memberName');
  const feedback = document.getElementById('memberFeedback');

  if (!memberNo) return;

  nameField.value = '';
  feedback.textContent = 'Looking up member...';

  fetch(`/admin/members/lookup/${memberNo}`)
    .then(res => res.json())
    .then(data => {
      if (data.found) {
        nameField.value = data.name;
        feedback.textContent = '';
      } else {
        feedback.textContent = 'Member not found';
        feedback.classList.add('text-danger');
      }
    })
    .catch(() => {
      feedback.textContent = 'Error looking up member';
      feedback.classList.add('text-danger');
    });
}

function confirmPost() {
  const member = document.getElementById('memberName').value || 'Unknown member';

  return confirm(
    `Confirm transaction posting:\n\n` +
    `Member: ${member}\n\n` +
    `This action cannot be undone.`
  );
}
