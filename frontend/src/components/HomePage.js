import React, { useState, useEffect } from 'react';
import { Button } from './ui/button';
import { Card, CardContent, CardHeader, CardTitle } from './ui/card';
import { Badge } from './ui/badge';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { 
  Home, 
  ShoppingCart, 
  Building, 
  TrendingUp, 
  Phone, 
  Mail, 
  MessageCircle, 
  CheckCircle, 
  Users, 
  Award, 
  Target,
  MapPin,
  BedDouble,
  Car,
  Maximize
} from 'lucide-react';
import { mockProperties } from '../data/mockData';

const HomePage = () => {
  const [isVisible, setIsVisible] = useState({});

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setIsVisible(prev => ({ ...prev, [entry.target.id]: true }));
          }
        });
      },
      { threshold: 0.1 }
    );

    const elements = document.querySelectorAll('[id]');
    elements.forEach((el) => observer.observe(el));

    return () => observer.disconnect();
  }, []);

  const whatsappNumber = "+919443246742"; // Velan Properties WhatsApp
  const whatsappMessage = "Hi! I'm interested in your real estate services. Can you help me?";
  const whatsappLink = `https://wa.me/${whatsappNumber.replace('+', '')}?text=${encodeURIComponent(whatsappMessage)}`;

  const handleFormSubmit = (e) => {
    e.preventDefault();
    // Mock form submission - would integrate with backend later
    alert('Thank you for your inquiry! We will contact you soon.');
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="fixed top-0 w-full bg-white/90 backdrop-blur-md z-50 border-b border-gray-100">
        <div className="container mx-auto px-4 py-4">
          <nav className="flex items-center justify-between">
            <div className="text-2xl font-bold text-royal-blue">
              Velan <span className="text-gold">Properties</span>
            </div>
            <div className="hidden md:flex items-center space-x-8">
              <a href="#home" className="text-gray-700 hover:text-royal-blue transition-colors">Home</a>
              <a href="#about" className="text-gray-700 hover:text-royal-blue transition-colors">About</a>
              <a href="#services" className="text-gray-700 hover:text-royal-blue transition-colors">Services</a>
              <a href="#properties" className="text-gray-700 hover:text-royal-blue transition-colors">Properties</a>
              <a href="#contact" className="text-gray-700 hover:text-royal-blue transition-colors">Contact</a>
            </div>
            <Button 
              onClick={() => window.open(whatsappLink, '_blank')}
              className="bg-green-500 hover:bg-green-600 text-white"
            >
              <MessageCircle className="w-4 h-4 mr-2" />
              WhatsApp
            </Button>
          </nav>
        </div>
      </header>

      {/* Hero Section */}
      <section id="home" className="relative min-h-screen flex items-center justify-center overflow-hidden">
        <div 
          className="absolute inset-0 bg-cover bg-center bg-no-repeat"
          style={{
            backgroundImage: 'url("https://images.unsplash.com/photo-1564013799919-ab600027ffc6?auto=format&fit=crop&w=1920&q=80")'
          }}
        />
        <div className="absolute inset-0 bg-black/40" />
        <div className="relative z-10 text-center text-white max-w-4xl mx-auto px-4">
          <h1 className={`text-5xl md:text-7xl font-bold mb-6 transform transition-all duration-1000 ${isVisible.home ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            Your Trusted Partner in <span className="text-gold">Real Estate</span>
          </h1>
          <p className={`text-xl md:text-2xl mb-8 transform transition-all duration-1000 delay-300 ${isVisible.home ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            Find your dream home with our expert guidance and transparent service
          </p>
          <div className={`flex flex-col sm:flex-row gap-4 justify-center transform transition-all duration-1000 delay-500 ${isVisible.home ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            <Button 
              onClick={() => window.open(whatsappLink, '_blank')}
              size="lg" 
              className="bg-green-500 hover:bg-green-600 text-white px-8 py-6 text-lg"
            >
              <MessageCircle className="w-5 h-5 mr-2" />
              Chat on WhatsApp
            </Button>
            <Button 
              onClick={() => document.getElementById('properties').scrollIntoView({ behavior: 'smooth' })}
              variant="outline" 
              size="lg" 
              className="border-white text-white hover:bg-white hover:text-royal-blue px-8 py-6 text-lg"
            >
              Explore Properties
            </Button>
          </div>
        </div>
      </section>

      {/* About Section */}
      <section id="about" className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className={`text-center mb-16 transform transition-all duration-1000 ${isVisible.about ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            <h2 className="text-4xl md:text-5xl font-bold text-royal-blue mb-6">About Velan Properties</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
              We are a trusted real estate service provider committed to helping you find the perfect property. 
              With years of experience and local expertise, we ensure transparent, reliable, and smart investment solutions.
            </p>
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {[
              { icon: Users, title: "Expert Team", desc: "Professional real estate experts at your service" },
              { icon: Award, title: "Trusted Service", desc: "Proven track record of successful transactions" },
              { icon: Target, title: "Smart Investments", desc: "Strategic guidance for profitable real estate decisions" }
            ].map((item, index) => (
              <Card key={index} className={`text-center p-6 hover:shadow-xl transition-all duration-500 transform ${isVisible.about ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`} style={{ transitionDelay: `${index * 200}ms` }}>
                <CardContent className="pt-6">
                  <item.icon className="w-16 h-16 text-gold mx-auto mb-4" />
                  <h3 className="text-xl font-semibold text-royal-blue mb-2">{item.title}</h3>
                  <p className="text-gray-600">{item.desc}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section id="services" className="py-20">
        <div className="container mx-auto px-4">
          <div className={`text-center mb-16 transform transition-all duration-1000 ${isVisible.services ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            <h2 className="text-4xl md:text-5xl font-bold text-royal-blue mb-6">Our Services</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Comprehensive real estate solutions tailored to your needs
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { icon: Home, title: "Buy", desc: "Find your perfect home with our expert guidance", color: "bg-blue-50 hover:bg-blue-100" },
              { icon: ShoppingCart, title: "Sell", desc: "Get the best value for your property", color: "bg-green-50 hover:bg-green-100" },
              { icon: Building, title: "Rent", desc: "Quality rental properties for every budget", color: "bg-purple-50 hover:bg-purple-100" },
              { icon: TrendingUp, title: "Invest", desc: "Smart investment opportunities in real estate", color: "bg-amber-50 hover:bg-amber-100" }
            ].map((service, index) => (
              <Card key={index} className={`${service.color} border-none hover:shadow-xl transition-all duration-500 cursor-pointer transform ${isVisible.services ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`} style={{ transitionDelay: `${index * 150}ms` }}>
                <CardHeader className="text-center">
                  <service.icon className="w-12 h-12 text-royal-blue mx-auto mb-4" />
                  <CardTitle className="text-xl text-royal-blue">{service.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-600 text-center">{service.desc}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Featured Properties */}
      <section id="properties" className="py-20 bg-gray-50">
        <div className="container mx-auto px-4">
          <div className={`text-center mb-16 transform transition-all duration-1000 ${isVisible.properties ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            <h2 className="text-4xl md:text-5xl font-bold text-royal-blue mb-6">Featured Properties</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Discover our handpicked selection of premium properties
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
            {mockProperties.map((property, index) => (
              <Card key={property.id} className={`overflow-hidden hover:shadow-2xl transition-all duration-500 cursor-pointer transform ${isVisible.properties ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`} style={{ transitionDelay: `${index * 200}ms` }}>
                <div className="relative overflow-hidden">
                  <img 
                    src={property.image} 
                    alt={property.title}
                    className="w-full h-64 object-cover transition-transform duration-500 hover:scale-110"
                  />
                  <Badge className="absolute top-4 left-4 bg-gold text-white">{property.type}</Badge>
                  <div className="absolute top-4 right-4 bg-royal-blue text-white px-3 py-1 rounded-full text-sm font-semibold">
                    ${property.price}
                  </div>
                </div>
                <CardContent className="p-6">
                  <h3 className="text-xl font-semibold text-royal-blue mb-2">{property.title}</h3>
                  <div className="flex items-center text-gray-600 mb-3">
                    <MapPin className="w-4 h-4 mr-1" />
                    <span className="text-sm">{property.location}</span>
                  </div>
                  <div className="flex items-center justify-between text-sm text-gray-500">
                    <div className="flex items-center">
                      <BedDouble className="w-4 h-4 mr-1" />
                      <span>{property.bedrooms} Beds</span>
                    </div>
                    <div className="flex items-center">
                      <Car className="w-4 h-4 mr-1" />
                      <span>{property.parking} Parking</span>
                    </div>
                    <div className="flex items-center">
                      <Maximize className="w-4 h-4 mr-1" />
                      <span>{property.area}</span>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section id="why-choose-us" className="py-20">
        <div className="container mx-auto px-4">
          <div className={`text-center mb-16 transform transition-all duration-1000 ${isVisible['why-choose-us'] ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            <h2 className="text-4xl md:text-5xl font-bold text-royal-blue mb-6">Why Choose Velan Properties?</h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Your success is our commitment
            </p>
          </div>
          <div className="max-w-4xl mx-auto">
            {[
              { icon: CheckCircle, title: "Trusted Service", desc: "Years of reliable and transparent service in real estate" },
              { icon: CheckCircle, title: "Local Expertise", desc: "Deep knowledge of local market trends and opportunities" },
              { icon: CheckCircle, title: "Smart Investments", desc: "Strategic guidance for profitable real estate decisions" },
              { icon: CheckCircle, title: "24/7 Support", desc: "Always available to assist you with any queries or concerns" }
            ].map((item, index) => (
              <div key={index} className={`flex items-start mb-8 p-6 bg-white rounded-lg shadow-lg hover:shadow-xl transition-all duration-500 transform ${isVisible['why-choose-us'] ? 'translate-x-0 opacity-100' : 'translate-x-10 opacity-0'}`} style={{ transitionDelay: `${index * 200}ms` }}>
                <item.icon className="w-8 h-8 text-green-500 mr-4 mt-1 flex-shrink-0" />
                <div>
                  <h3 className="text-xl font-semibold text-royal-blue mb-2">{item.title}</h3>
                  <p className="text-gray-600">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section id="contact" className="py-20 bg-royal-blue text-white">
        <div className="container mx-auto px-4">
          <div className={`text-center mb-16 transform transition-all duration-1000 ${isVisible.contact ? 'translate-y-0 opacity-100' : 'translate-y-10 opacity-0'}`}>
            <h2 className="text-4xl md:text-5xl font-bold mb-6">Get In Touch</h2>
            <p className="text-xl max-w-3xl mx-auto opacity-90">
              Ready to find your dream property? Contact us today!
            </p>
          </div>
          <div className="grid lg:grid-cols-2 gap-12 max-w-6xl mx-auto">
            <div className={`transform transition-all duration-1000 ${isVisible.contact ? 'translate-x-0 opacity-100' : '-translate-x-10 opacity-0'}`}>
              <h3 className="text-2xl font-semibold mb-6">Contact Information</h3>
              <div className="space-y-4">
                <div className="flex items-center">
                  <Phone className="w-6 h-6 mr-4 text-gold" />
                  <span className="text-lg">+919443246742</span>
                </div>
                <div className="flex items-center">
                  <Mail className="w-6 h-6 mr-4 text-gold" />
                  <span className="text-lg">velanproperties777@gmail.com</span>
                </div>
                <div className="flex items-center">
                  <MapPin className="w-6 h-6 mr-4 text-gold" />
                  <span className="text-lg">123 Real Estate Avenue, Property City</span>
                </div>
              </div>
              <div className="mt-8">
                <Button 
                  onClick={() => window.open(whatsappLink, '_blank')}
                  size="lg" 
                  className="bg-green-500 hover:bg-green-600 text-white px-8 py-4"
                >
                  <MessageCircle className="w-5 h-5 mr-2" />
                  Chat on WhatsApp Now
                </Button>
              </div>
            </div>
            <div className={`transform transition-all duration-1000 ${isVisible.contact ? 'translate-x-0 opacity-100' : 'translate-x-10 opacity-0'}`}>
              <form onSubmit={handleFormSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-4">
                  <Input 
                    placeholder="Your Name" 
                    required 
                    className="bg-white/10 border-white/20 text-white placeholder:text-white/70"
                  />
                  <Input 
                    type="email"
                    placeholder="Your Email" 
                    required 
                    className="bg-white/10 border-white/20 text-white placeholder:text-white/70"
                  />
                </div>
                <Input 
                  placeholder="Phone Number" 
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/70"
                />
                <Textarea 
                  placeholder="Your Message"
                  rows={5}
                  className="bg-white/10 border-white/20 text-white placeholder:text-white/70"
                />
                <Button 
                  type="submit"
                  size="lg" 
                  className="w-full bg-gold hover:bg-gold/90 text-royal-blue font-semibold"
                >
                  Send Message
                </Button>
              </form>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-4 gap-8">
            <div>
              <div className="text-2xl font-bold mb-4">
                Velan <span className="text-gold">Properties</span>
              </div>
              <p className="text-gray-400 mb-4">
                Your trusted partner in real estate, helping you find the perfect property.
              </p>
              <Button 
                onClick={() => window.open(whatsappLink, '_blank')}
                className="bg-green-500 hover:bg-green-600"
              >
                <MessageCircle className="w-4 h-4 mr-2" />
                WhatsApp
              </Button>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#home" className="hover:text-white transition-colors">Home</a></li>
                <li><a href="#about" className="hover:text-white transition-colors">About Us</a></li>
                <li><a href="#services" className="hover:text-white transition-colors">Services</a></li>
                <li><a href="#properties" className="hover:text-white transition-colors">Properties</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Services</h4>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white transition-colors">Buy Property</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Sell Property</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Rent Property</a></li>
                <li><a href="#" className="hover:text-white transition-colors">Investment</a></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Contact Info</h4>
              <div className="space-y-2 text-gray-400">
                <p>{whatsappNumber}</p>
                <p>info@velanproperties.com</p>
                <p>123 Real Estate Avenue<br />Property City</p>
              </div>
            </div>
          </div>
          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2024 Velan Properties. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;