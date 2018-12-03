
describe('VUE CRUD tests', () => {
  beforeEach(() => {
    cy.visit('localhost:8080')
  })

  it('tests adding a new user', () => {
    cy.contains('Add User').click()

    cy.get('#form-username-input').type('Max Mustermann')
    cy.get('#form-email-input').type('mmuster@gmail.at')
    cy.get('#form-picture-input').type('LinkZumAllerbestenPicture.png')

    cy.get('#addUserForm').submit()
  })

  it('tests updating the name of a user', () => {
    cy.get('table').contains('tr','Max Mustermann').contains('td','Update').click()

    cy.get('#form-username-edit-input').clear()
    cy.get('#form-username-edit-input').type('Max Mustermann 2')

    cy.get('#editUserForm').submit()
  })

  it('checks if old username does not exist anymore', () => {
    cy.get('table').contains('td','Max Mustermann').should('not.exist')
  })

  it('checks if new username exists now', () => {
    cy.get('table').contains('td','Max Mustermann 2')
  })

  it('deletes the test user', () => {
    cy.get('table')
    .contains('tr','Max Mustermann 2')
    .contains('td','Delete')
    .click()
  })

  it('Checks if testuser is gone', () => {
    cy.get('table')
    .contains('tr','Max Mustermann 2')
    .should('not.exist')
  })

})
