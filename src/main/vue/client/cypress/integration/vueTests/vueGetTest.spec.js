
describe('VUE CRUD tests', () => {
  beforeEach(() => {
    cy.visit('localhost:8080')
  })

  it('tests adding a new user', () => {
    cy.contains('Add User').click()

    cy.get('#form-username-input').type('Max Mustermann')
    cy.get('#form-email-input').type('mmuster@gmail.at')
    cy.get('#form-picture-input').type('LinkZumAllerbestenPicture')

    cy.contains('Submit').click()
  })

  it('tests updating the name of a user', () => {
    cy.get('table').contains('tr','Max Mustermann').contains('td','Update').click()

    cy.get('#form-username-edit-input').clear()
    cy.get('#form-username-edit-input').type('Max Mustermann 2')

    
    cy.get('#user-update-modal').get('#edit-form-submit-button').click()
  })

  it('checks if old username does not exist anymore', () => {
    cy.get('table').contains('td','Max Mustermann').should('not.exist')
  })

  it('checks if new username exists now', () => {
    cy.get('table').contains('td','Max Mustermann 2')
  })

  it('deletes the test user and checks if it is not there anymore', () => {
    cy.get('table')
    .contains('tr','Max Mustermann 2')
    .contains('td','Delete')
    .click()

    cy.get('table')
    .contains('tr','Max Mustermann 2')
    .should('not.exist')
  })
})
