describe('First Battlesnake test', () => {
  before(() => {
    // Hide the Django toolbar if it's showing
    // and move it down the page so it doesn't block any elements
    cy.setCookie('djdt', 'hide')
    cy.setCookie('djdttop', '600')
  })

  beforeEach(() => {
    Cypress.Cookies.preserveOnce('djdt', 'djdttop')

    cy.visit('/')
  })

  it('should show the page to login', () => {
    cy.getCookie('sessionid').should('not.exist')
    cy.get('a')
      .contains('Login')
      .click()
    cy.url().should('contain', '/login/')
    cy.get('a')
      .contains('Sign in with GitHub')
      .should('have.attr', 'href', '/oauth/login/github/?next=')
  })
})
