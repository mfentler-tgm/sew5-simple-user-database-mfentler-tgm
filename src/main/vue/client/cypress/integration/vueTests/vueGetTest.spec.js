
describe('vueGetTest', () => {
  beforeEach(() => {
    cy.visit('localhost:8080')
  })

  it('tests if the table is there', () =>{
    cy.contains('Username')
  })

  it('inserts a testuser', () => {
    cy.request('POST','localhost:5000/user', {'username':'Max Mustermann', 'email':'mmuster@musteremail.com', 'picture':'linkkk'})
  })

  it('tests if new user is there', () => {
    cy.contains('Max Mustermann')
  })

  it('deletes the user again', () => {
    cy.request('DELETE','localhost:5000/user/3')
  })

  it('tests if user is still there', () => {
    cy.contains('Max Mustermann').should('not.exist')
  })
})
