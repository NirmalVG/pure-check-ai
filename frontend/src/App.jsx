import { BrowserRouter, Routes, Route, Link, NavLink } from "react-router-dom"
import { Navbar, Nav, Container } from "react-bootstrap"
import Home from "./pages/Home"
import Analyze from "./pages/Analyze"
import Encyclopedia from "./pages/Encyclopedia"
import Quiz from "./pages/Quiz"

const AppNavbar = () => {
  return (
    <Navbar
      expand="lg"
      className="pc-navbar"
      fixed="top"
      style={{
        backdropFilter: "blur(12px)",
        backgroundColor: "rgba(249,248,246,0.85)",
      }}
    >
      <Container>
        <Navbar.Brand as={Link} to="/">
          <i className="bi bi-stars me-2"></i>
          PureCheck AI
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="main-nav" />
        <Navbar.Collapse id="main-nav">
          <Nav className="mx-auto">
            <Nav.Link as={NavLink} to="/analyze">
              Analysis
            </Nav.Link>
            <Nav.Link as={NavLink} to="/ingredients">
              Ingredients
            </Nav.Link>
            <Nav.Link as={NavLink} to="/quiz">
              Quiz
            </Nav.Link>
          </Nav>
          <Link to="/analyze" className="btn btn-pc-primary btn-sm">
            Get Started
          </Link>
        </Navbar.Collapse>
      </Container>
    </Navbar>
  )
}

const Footer = () => {
  return (
    <footer className="pc-footer">
      <Container>
        <div className="row">
          <div className="col-md-4 mb-4">
            <div
              className="mb-3"
              style={{
                fontFamily: "var(--pc-font-serif)",
                fontWeight: 700,
                fontSize: "1.3rem",
              }}
            >
              <i className="bi bi-stars me-2"></i>PureCheck AI
            </div>
            <p style={{ maxWidth: 300 }}>
              The world's most sophisticated cosmetic ingredient analyzer.
              Dedicated to transparency in the beauty industry.
            </p>
          </div>
          <div className="col-md-2 offset-md-2 mb-4">
            <h6>Platform</h6>
            <Link to="/">How it Works</Link>
            <Link to="/">Pricing</Link>
            <Link to="/">API Access</Link>
          </div>
          <div className="col-md-2 mb-4">
            <h6>Company</h6>
            <Link to="/">Science Board</Link>
            <Link to="/">Privacy Policy</Link>
            <Link to="/">Terms of Service</Link>
          </div>
        </div>
        <hr style={{ borderColor: "var(--pc-border)" }} />
        <div className="d-flex justify-content-between align-items-center">
          <small>© 2026 PureCheck AI. All rights reserved.</small>
          <div className="d-flex gap-3">
            <i className="bi bi-globe2"></i>
            <i className="bi bi-envelope"></i>
          </div>
        </div>
      </Container>
    </footer>
  )
}

function App() {
  return (
    <BrowserRouter>
      <AppNavbar />
      <main style={{ paddingTop: "80px", minHeight: "100vh" }}>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/analyze" element={<Analyze />} />
          <Route path="/ingredients" element={<Encyclopedia />} />
          <Route path="/quiz" element={<Quiz />} />
        </Routes>
      </main>
      <Footer />
    </BrowserRouter>
  )
}

export default App
