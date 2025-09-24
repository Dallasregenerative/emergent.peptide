import React, { useState, useEffect, useRef, Suspense, lazy, useCallback } from "react";
import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import axios from "axios";
import { Button } from "./components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./components/ui/card";
import { Input } from "./components/ui/input";
import { Label } from "./components/ui/label";
import { Textarea } from "./components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "./components/ui/select";
import { Badge } from "./components/ui/badge";
import { Separator } from "./components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./components/ui/tabs";
import { Progress } from "./components/ui/progress";
import { AlertCircle, Brain, FileText, User, Zap, Upload, Search, BookOpen, Download, CheckCircle, XCircle, Clock, MessageCircle, Stethoscope, FlaskConical, Activity, Shield, Users, Network, Award, TrendingUp, Eye, Lock, Star, AlertTriangle, Filter, Menu, X, Calculator, Pill, Layers } from "lucide-react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar, PieChart, Pie, Cell, AreaChart, Area, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { format, parseISO, subDays, startOfWeek, endOfWeek } from 'date-fns';
import { Alert, AlertDescription } from "./components/ui/alert";
import ProgressTracking from "./components/ProgressTracking";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API = `${BACKEND_URL}/api`;

const PeptideProtocolsApp = () => {
  const [currentView, setCurrentView] = useState('home');
  const [currentStep, setCurrentStep] = useState(1);
  const [assessmentId, setAssessmentId] = useState(null);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isAutoSaving, setIsAutoSaving] = useState(false);
  const [assessment, setAssessment] = useState({
    patient_name: '',
    age: '',
    gender: '',
    weight: '',
    height_feet: '',
    height_inches: '',
    email: '',
    primary_concerns: [],
    health_goals: [],
    current_medications: [],
    lifestyle_factors: {},
    medical_history: [],
    allergies: []
  });
  const [generatedProtocol, setGeneratedProtocol] = useState(null);
  const [loading, setLoading] = useState(false);
  const [protocolLibrary, setProtocolLibrary] = useState([]);
  const [peptidesDatabase, setPeptidesDatabase] = useState([]);
  const [peptideCategories, setPeptideCategories] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [selectedPeptide, setSelectedPeptide] = useState(null);
  const [chatMessages, setChatMessages] = useState([]);
  const [chatInput, setChatInput] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [accessCode, setAccessCode] = useState('');
  const [protocolProgress, setProtocolProgress] = useState(null);
  const chatInputRef = useRef(null);
  const fullNameRef = useRef(null);
  const weightRef = useRef(null);
  const autoSaveTimeoutRef = useRef(null);

  // Feedback System State
  const [showFeedbackChat, setShowFeedbackChat] = useState(false);
  const [showProtocolFeedback, setShowProtocolFeedback] = useState(false);
  const [showErrorReport, setShowErrorReport] = useState(false);
  const [feedbackChatResponse, setFeedbackChatResponse] = useState('');
  const [loadingFeedbackChat, setLoadingFeedbackChat] = useState(false);
  const [protocolRating, setProtocolRating] = useState(0);
  const [improvementsNoticed, setImprovementsNoticed] = useState([]);
  const [protocolFeedbackResponse, setProtocolFeedbackResponse] = useState('');
  const [loadingProtocolFeedback, setLoadingProtocolFeedback] = useState(false);
  const [errorReportResponse, setErrorReportResponse] = useState('');
  const [loadingErrorReport, setLoadingErrorReport] = useState(false);
  
  // Feedback refs
  const feedbackChatInputRef = useRef(null);
  const sideEffectsRef = useRef(null);
  const additionalFeedbackRef = useRef(null);
  const errorTypeRef = useRef(null);
  const incorrectInfoRef = useRef(null);
  const correctInfoRef = useRef(null);
  const severityRef = useRef(null);

  // Auto-save functionality
  const saveToLocalStorage = (assessmentData, step, assessmentIdLocal) => {
    try {
      const saveData = {
        assessment: assessmentData,
        currentStep: step,
        assessmentId: assessmentIdLocal,
        timestamp: new Date().toISOString(),
        lastSaved: Date.now()
      };
      localStorage.setItem('peptideAssessmentDraft', JSON.stringify(saveData));
      console.log('Assessment auto-saved to localStorage');
    } catch (error) {
      console.error('Failed to save to localStorage:', error);
    }
  };

  const loadFromLocalStorage = () => {
    try {
      const saved = localStorage.getItem('peptideAssessmentDraft');
      if (saved) {
        const saveData = JSON.parse(saved);
        // Only load if saved within last 7 days
        if (Date.now() - saveData.lastSaved < 7 * 24 * 60 * 60 * 1000) {
          return saveData;
        } else {
          // Remove expired save
          localStorage.removeItem('peptideAssessmentDraft');
        }
      }
    } catch (error) {
      console.error('Failed to load from localStorage:', error);
      localStorage.removeItem('peptideAssessmentDraft'); // Remove corrupted data
    }
    return null;
  };

  const clearAutoSave = () => {
    try {
      localStorage.removeItem('peptideAssessmentDraft');
      console.log('Assessment draft cleared from localStorage');
    } catch (error) {
      console.error('Failed to clear localStorage:', error);
    }
  };

  const autoSave = async (assessmentData, step, assessmentIdLocal) => {
    // Always save to localStorage for instant recovery
    saveToLocalStorage(assessmentData, step, assessmentIdLocal);
    
    // Also try to save to server if we have an assessment ID
    if (assessmentIdLocal && !isAutoSaving) {
      setIsAutoSaving(true);
      try {
        await saveAssessmentStep(step, assessmentData);
      } catch (error) {
        console.warn('Server auto-save failed, localStorage backup available:', error);
      } finally {
        setIsAutoSaving(false);
      }
    }
  };

  const handleAssessmentChange = useCallback((field, value) => {
    setAssessment(prev => ({
      ...prev,
      [field]: value
    }));
    
    // Debounced auto-save - only save after user stops typing
    if (autoSaveTimeoutRef.current) {
      clearTimeout(autoSaveTimeoutRef.current);
    }
    autoSaveTimeoutRef.current = setTimeout(() => {
      setAssessment(currentAssessment => {
        const updatedAssessment = {
          ...currentAssessment,
          [field]: value
        };
        autoSave(updatedAssessment, currentStep, assessmentId);
        return currentAssessment; // Don't update state again
      });
    }, 1000); // Wait 1 second after user stops typing
  }, [currentStep, assessmentId]);

  const handleLifestyleFactorChange = (factor, value) => {
    const updatedAssessment = {
      ...assessment,
      lifestyle_factors: {
        ...assessment.lifestyle_factors,
        [factor]: value
      }
    };
    setAssessment(updatedAssessment);
    
    // Debounced auto-save
    if (autoSaveTimeoutRef.current) {
      clearTimeout(autoSaveTimeoutRef.current);
    }
    autoSaveTimeoutRef.current = setTimeout(() => {
      autoSave(updatedAssessment, currentStep, assessmentId);
    }, 1000);
  };

  const addToListField = (field, value) => {
    if (value.trim()) {
      setAssessment(prev => ({
        ...prev,
        [field]: [...prev[field], value.trim()]
      }));
    }
  };

  const removeFromListField = (field, index) => {
    setAssessment(prev => ({
      ...prev,
      [field]: prev[field].filter((_, i) => i !== index)
    }));
  };

  const saveAssessmentStep = async (step, data) => {
    try {
      setLoading(true);
      console.log('Saving assessment step:', step, 'with data:', data);
      console.log('Current assessmentId:', assessmentId);
      
      const response = await axios.post(`${API}/assessment/multi-step${assessmentId ? `?assessment_id=${assessmentId}` : ''}`, {
        step,
        assessment_data: data
      });
      
      console.log('Assessment step save response:', response.data);
      
      if (!assessmentId) {
        setAssessmentId(response.data.id);
        console.log('Setting new assessmentId:', response.data.id);
      }
      
      return response.data;
    } catch (error) {
      console.error('Error saving assessment step:', error);
      console.error('Error details:', error.response?.data);
      alert('Error saving assessment. Please try again.');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (files) => {
    if (!assessmentId) {
      alert('Please complete basic information first');
      return;
    }

    const formData = new FormData();
    Array.from(files).forEach(file => {
      formData.append('files', file);
    });

    try {
      setLoading(true);
      const response = await axios.post(`${API}/assessment/${assessmentId}/upload-files`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setUploadedFiles(prev => [...prev, ...response.data.analyses]);
      alert(`Successfully uploaded and analyzed ${files.length} files!`);
    } catch (error) {
      console.error('File upload error:', error);
      alert('Error uploading files. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const generateFunctionalProtocol = async () => {
    if (!assessmentId) {
      alert('Please complete the assessment first');
      return;
    }

    setLoading(true);
    console.log('🔄 Starting protocol generation for assessment:', assessmentId);
    
    try {
      console.log('📤 Making API call to generate protocol...');
      
      // Set longer timeout for protocol generation (3 minutes) and add progress feedback
      const timeoutMs = 180000; // 3 minutes
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
      
      // Show progress messages to user
      let progressMessage = "Generating your personalized protocol...";
      setProtocolProgress(progressMessage);
      
      const progressInterval = setInterval(() => {
        const messages = [
          "Analyzing your health assessment...",
          "Selecting optimal peptide protocols...", 
          "Calculating personalized dosing...",
          "Generating clinical recommendations...",
          "Finalizing your comprehensive protocol..."
        ];
        const randomMessage = messages[Math.floor(Math.random() * messages.length)];
        setProtocolProgress(randomMessage);
      }, 10000); // Update every 10 seconds
      
      const response = await axios.post(`${API}/generate-functional-protocol/${assessmentId}`, {}, {
        signal: controller.signal,
        timeout: timeoutMs
      });
      
      clearTimeout(timeoutId);
      clearInterval(progressInterval);
      
      console.log('✅ Protocol generation response received:', response.status);
      console.log('📊 Response data structure:', Object.keys(response.data));
      
      if (response.data && response.data.protocol) {
        console.log('✅ Setting generated protocol:', response.data.protocol);
        setGeneratedProtocol(response.data.protocol);
        console.log('✅ Setting view to protocol');
        setCurrentView('protocol');
        setProtocolProgress(null);
        console.log('✅ State updates complete');
      } else {
        console.error('❌ No protocol in response data');
        setProtocolProgress(null);
        alert('Error: No protocol data received from server. Please try again.');
      }
    } catch (error) {
      console.error('❌ Protocol generation error:', error);
      setProtocolProgress(null);
      
      if (error.name === 'AbortError') {
        alert('Protocol generation is taking longer than expected. Please try again or contact support if this persists.');
      } else if (error.code === 'ECONNABORTED' || error.message.includes('timeout')) {
        alert('Protocol generation timed out. Our servers are processing your request - please try again in a few minutes.');
      } else {
        alert(`Error generating protocol: ${error.response?.data?.detail || error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const chatWithDrPeptide = async (message) => {
    setChatLoading(true);
    
    // Add user message to chat
    const userMessage = { role: 'user', content: message };
    setChatMessages(prev => [...prev, userMessage]);

    try {
      const response = await axios.post(`${API}/dr-peptide/chat`, {
        message,
        conversation_history: chatMessages
      });

      if (response.data.success) {
        const aiMessage = { role: 'assistant', content: response.data.response };
        setChatMessages(prev => [...prev, aiMessage]);
      } else {
        const errorMessage = { role: 'assistant', content: response.data.response || 'Sorry, I encountered an error.' };
        setChatMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = { role: 'assistant', content: 'I apologize, but I\'m experiencing technical difficulties right now.' };
      setChatMessages(prev => [...prev, errorMessage]);
    } finally {
      setChatLoading(false);
      setChatInput('');
    }
  };

  const loadEnhancedProtocolLibrary = async () => {
    try {
      const response = await axios.get(`${API}/enhanced-library`);
      setProtocolLibrary(response.data);
    } catch (error) {
      console.error('Error loading enhanced library:', error);
      // Fallback to basic library
      try {
        const basicResponse = await axios.get(`${API}/library`);
        setProtocolLibrary(basicResponse.data);
      } catch (fallbackError) {
        console.error('Error loading basic library:', error);
      }
    }
  };

  const loadPeptidesDatabase = async () => {
    try {
      const [peptidesResponse, categoriesResponse] = await Promise.all([
        axios.get(`${API}/peptides`),
        axios.get(`${API}/peptides/categories`)
      ]);
      setPeptidesDatabase(peptidesResponse.data);
      setPeptideCategories(categoriesResponse.data.categories);
    } catch (error) {
      console.error('Error loading peptides database:', error);
    }
  };

  useEffect(() => {
    if (currentView === 'protocols' || currentView === 'library') {
      loadEnhancedProtocolLibrary();
    }
    if (currentView === 'peptides') {
      loadPeptidesDatabase();
    }
  }, [currentView]);

  // Auto-save restore effect
  useEffect(() => {
    if (currentView === 'assessment') {
      const saved = loadFromLocalStorage();
      if (saved && !assessmentId) {
        // Auto-restore without confirmation for better UX
        console.log('Auto-restoring saved assessment data');
        setAssessment(saved.assessment);
        setCurrentStep(saved.currentStep);
        setAssessmentId(saved.assessmentId);
        console.log('Assessment auto-restored from localStorage');
      }
    }
  }, [currentView, assessmentId]);

  // Feedback System Functions
  const sendFeedbackChat = async () => {
    const message = feedbackChatInputRef.current?.value;
    if (!message || !message.trim()) return;

    try {
      setLoadingFeedbackChat(true);
      const response = await axios.post(`${API}/dr-peptide/feedback-chat`, {
        message: message.trim(),
        protocol_id: "sample_protocol", // Would be actual protocol ID
        feedback_context: {}
      });

      if (response.data.success) {
        setFeedbackChatResponse(response.data.response);
        if (feedbackChatInputRef.current) {
          feedbackChatInputRef.current.value = '';
        }
      }
    } catch (error) {
      console.error('Error sending feedback chat:', error);
      setFeedbackChatResponse('Sorry, there was an error processing your message. Please try again.');
    } finally {
      setLoadingFeedbackChat(false);
    }
  };

  const submitProtocolFeedback = async () => {
    try {
      setLoadingProtocolFeedback(true);
      
      const feedbackData = {
        protocol_id: "sample_protocol", // Would be actual protocol ID
        feedback_data: {
          protocol_effectiveness: protocolRating,
          specific_outcomes: {
            improvements_noticed: improvementsNoticed,
            side_effects: sideEffectsRef.current?.value || ""
          },
          days_since_start: 30, // Would be calculated
          additional_feedback: additionalFeedbackRef.current?.value || ""
        }
      };

      const response = await axios.post(`${API}/feedback/protocol`, feedbackData);
      
      if (response.data.success) {
        setProtocolFeedbackResponse(response.data.dr_peptide_response);
      }
    } catch (error) {
      console.error('Error submitting protocol feedback:', error);
      setProtocolFeedbackResponse('Thank you for your feedback! We encountered a technical issue but your feedback has been recorded.');
    } finally {
      setLoadingProtocolFeedback(false);
    }
  };

  const submitErrorReport = async () => {
    try {
      setLoadingErrorReport(true);
      
      const reportData = {
        incorrect_content: incorrectInfoRef.current?.value || "",
        corrected_content: correctInfoRef.current?.value || "",
        reporter_type: "user",
        severity: severityRef.current?.value || "medium",
        context: errorTypeRef.current?.value || ""
      };

      const response = await axios.post(`${API}/feedback/error-correction`, reportData);
      
      if (response.data.success) {
        setErrorReportResponse(response.data.dr_peptide_response);
      }
    } catch (error) {
      console.error('Error submitting error report:', error);
      setErrorReportResponse('Thank you for reporting this issue. We have received your report and will review it promptly.');
    } finally {
      setLoadingErrorReport(false);
    }
  };

  const ListFieldInput = ({ field, placeholder, label }) => {
    const [inputValue, setInputValue] = useState('');
    
    return (
      <div className="space-y-2">
        <Label className="text-sm font-medium">{label}</Label>
        <div className="flex gap-2">
          <Input
            placeholder={placeholder}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
                addToListField(field, inputValue);
                setInputValue('');
              }
            }}
          />
          <Button
            type="button"
            variant="outline"
            onClick={() => {
              addToListField(field, inputValue);
              setInputValue('');
            }}
          >
            Add
          </Button>
        </div>
        <div className="flex flex-wrap gap-1">
          {assessment[field].map((item, index) => (
            <Badge
              key={index}
              variant="secondary"
              className="cursor-pointer"
              onClick={() => removeFromListField(field, index)}
            >
              {item} ✕
            </Badge>
          ))}
        </div>
      </div>
    );
  };

  const HomePage = () => (
    <div className="min-h-screen bg-gradient-to-br from-blue-900 via-blue-800 to-purple-900">
      {/* Hero Section */}
      <div className="container mx-auto px-4 md:px-6 py-8 md:py-12">
        <div className="text-center space-y-6 md:space-y-8">
          <div className="flex flex-col md:flex-row items-center justify-center gap-4 mb-6 md:mb-8">
            <div className="relative">
              <Brain className="h-12 w-12 md:h-16 md:w-16 text-blue-400" />
              <div className="absolute -top-1 md:-top-2 -right-1 md:-right-2 bg-green-400 rounded-full p-1">
                <Stethoscope className="h-4 w-4 md:h-6 md:w-6 text-white" />
              </div>
            </div>
            <div className="text-center md:text-left">
              <h1 className="text-3xl md:text-6xl font-bold text-white mb-2">
                👋 Hi! I'm Dr. Peptide
              </h1>
              <p className="text-lg md:text-2xl text-blue-200">Your AI Peptide Therapy Expert</p>
            </div>
          </div>

          {/* Chat with Dr. Peptide - Directly under header */}
          <Card className="max-w-md mx-auto mb-8 md:mb-12 bg-white/10 backdrop-blur border-white/20">
            <CardHeader>
              <CardTitle className="text-white flex items-center gap-2">
                <MessageCircle className="h-5 w-5" />
                Chat with Dr. Peptide
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="bg-blue-600 text-white p-3 rounded-lg text-sm">
                  Hello! I'm Dr. Peptide. I can help you understand peptide therapy, interpret your lab results, and create personalized protocols. What can I help you with today?
                </div>
                <Button 
                  onClick={() => setCurrentView('chat')}
                  className="w-full"
                >
                  Start Chatting
                </Button>
              </div>
            </CardContent>
          </Card>
          
          <h2 className="text-3xl md:text-5xl font-bold text-white mb-4 md:mb-6">
            Clinical-Grade Peptide Protocols
          </h2>
          
          <p className="text-base md:text-xl text-blue-100 max-w-4xl mx-auto mb-8 md:mb-12 px-4">
            Experience personalized peptide therapy with evidence-based protocols generated by advanced AI and validated by expert practitioners worldwide. HIPAA-compliant and clinically proven.
          </p>

          {/* Updated button stack */}
          <div className="flex flex-col gap-4 justify-center mb-12 md:mb-16 px-4 max-w-md mx-auto">
            <Button 
              onClick={() => setCurrentView('assessment')}
              className="bg-green-600 hover:bg-green-700 text-white px-6 md:px-8 py-3 md:py-4 text-base md:text-lg font-semibold rounded-full w-full"
            >
              🚀 Generate Personalized Protocol
            </Button>
            <Button 
              onClick={() => setCurrentView('peptides')}
              variant="outline"
              className="border-white text-white hover:bg-white hover:text-blue-900 px-6 md:px-8 py-3 md:py-4 text-base md:text-lg font-semibold rounded-full w-full"
            >
              View Peptides Library
            </Button>
            <Button 
              onClick={() => setCurrentView('protocols')}
              variant="outline"
              className="border-white text-white hover:bg-white hover:text-blue-900 px-6 md:px-8 py-3 md:py-4 text-base md:text-lg font-semibold rounded-full w-full"
            >
              View Protocols Library
            </Button>
          </div>

          {/* Statistics - Option 2: Ambitious & Justified */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8 mb-12 md:mb-16 px-4">
            <div className="text-center">
              <div className="text-2xl md:text-4xl font-bold text-white">2,800+</div>
              <div className="text-sm md:text-base text-blue-200">Studies Analyzed</div>
              <div className="text-xs text-blue-300 mt-1">AI synthesis of global peptide research literature</div>
            </div>
            <div className="text-center">
              <div className="text-2xl md:text-4xl font-bold text-white">390+</div>
              <div className="text-sm md:text-base text-blue-200">Medical Conditions</div>
              <div className="text-xs text-blue-300 mt-1">Comprehensive coverage across all health areas</div>
            </div>
            <div className="text-center">
              <div className="text-2xl md:text-4xl font-bold text-white">16</div>
              <div className="text-sm md:text-base text-blue-200">AI Agents Collaborating</div>
              <div className="text-xs text-blue-300 mt-1">Revolutionary multi-intelligence platform</div>
            </div>
            <div className="text-center">
              <div className="text-2xl md:text-4xl font-bold text-white">24/7</div>
              <div className="text-sm md:text-base text-blue-200">Clinical Intelligence</div>
              <div className="text-xs text-blue-300 mt-1">World's first AI-powered peptide medicine platform</div>
            </div>
          </div>
        </div>

        {/* HIPAA Compliance */}
        <Card className="max-w-4xl mx-auto mb-12 bg-white/10 backdrop-blur border-white/20">
          <CardHeader>
            <CardTitle className="text-white flex items-center gap-2">
              <Shield className="h-6 w-6" />
              HIPAA Compliant Platform
            </CardTitle>
            <CardDescription className="text-blue-100">
              Your protected health information (PHI) is secured with enterprise-grade encryption and access controls that meet all HIPAA compliance requirements.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-blue-100">
                  <CheckCircle className="h-4 w-4 text-green-400" />
                  <span className="text-sm">End-to-end AES-256 encryption</span>
                </div>
                <div className="flex items-center gap-2 text-blue-100">
                  <CheckCircle className="h-4 w-4 text-green-400" />
                  <span className="text-sm">Comprehensive audit logging</span>
                </div>
              </div>
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-blue-100">
                  <CheckCircle className="h-4 w-4 text-green-400" />
                  <span className="text-sm">Role-based access controls</span>
                </div>
                <div className="flex items-center gap-2 text-blue-100">
                  <CheckCircle className="h-4 w-4 text-green-400" />
                  <span className="text-sm">SOC 2 Type II compliance</span>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Features Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-8 mt-16">
          <Card className="bg-white/10 backdrop-blur border-white/20">
            <CardContent className="p-6">
              <Activity className="h-8 w-8 text-blue-400 mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">AI-Powered Protocols</h3>
              <p className="text-blue-100">Advanced artificial intelligence generates personalized peptide therapy protocols based on your unique health profile.</p>
            </CardContent>
          </Card>

          <Card className="bg-white/10 backdrop-blur border-white/20">
            <CardContent className="p-6">
              <FlaskConical className="h-8 w-8 text-green-400 mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Lab Analysis</h3>
              <p className="text-blue-100">Upload your lab results, genetic tests, and medical charts for comprehensive AI analysis and personalized recommendations.</p>
            </CardContent>
          </Card>

          <Card className="bg-white/10 backdrop-blur border-white/20">
            <CardContent className="p-6">
              <Users className="h-8 w-8 text-purple-400 mb-4" />
              <h3 className="text-xl font-semibold text-white mb-2">Expert Network</h3>
              <p className="text-blue-100">Connect with verified medical professionals who specialize in peptide therapy and personalized medicine.</p>
            </CardContent>
          </Card>
        </div>

        {/* Call to Action */}
        <div className="text-center mt-16 space-y-6">
          <h3 className="text-3xl font-bold text-white">Ready to Begin Your Peptide Therapy Journey?</h3>
          <p className="text-xl text-blue-100">Join thousands of patients and practitioners using evidence-based peptide protocols</p>
          <div className="flex gap-4 justify-center">
            <Button 
              onClick={() => setCurrentView('assessment')}
              className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3"
            >
              Start Assessment
            </Button>
            <Button 
              onClick={() => setCurrentView('protocols')}
              variant="outline"
              className="border-white text-white hover:bg-white hover:text-blue-900 px-8 py-3"
            >
              Browse Protocols
            </Button>
            <Button 
              onClick={() => setCurrentView('network')}
              variant="outline"
              className="border-white text-white hover:bg-white hover:text-blue-900 px-8 py-3"
            >
              Join Network
            </Button>
          </div>
        </div>
      </div>
    </div>
  );

  const AssessmentWizard = () => (
    <div className="max-w-4xl mx-auto p-4 md:p-6 space-y-6 md:space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-2xl md:text-4xl font-bold">Intelligent Protocol Generator</h1>
        <p className="text-base md:text-lg text-gray-600">Advanced AI-powered peptide therapy protocols with evidence-based clinical recommendations.</p>
        
        <div className="flex justify-center gap-2 md:gap-4 text-sm">
          <Badge variant="outline">Evidence-Based</Badge>
          <Badge variant="outline">AI-Powered</Badge>
          <Badge variant="outline">Clinical Grade</Badge>
          {isAutoSaving && <Badge variant="outline" className="bg-blue-50">Auto-Saving...</Badge>}
        </div>
        
        {/* Auto-save status indicator */}
        <div className="text-xs text-gray-500 flex items-center justify-center gap-1">
          <CheckCircle className="h-3 w-3 text-green-500" />
          Your progress is automatically saved
        </div>
      </div>

      {/* Progress Bar */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm text-gray-600">
          <span>Step {currentStep} of 7</span>
          <span>{Math.round((currentStep / 7) * 100)}% Complete</span>
        </div>
        <Progress value={(currentStep / 7) * 100} className="w-full" />
      </div>

      {/* Step Headers */}
      <div className="flex flex-wrap justify-center gap-2 text-xs">
        {['Personal Information', 'Health Goals & Objectives', 'Medical History', 'Lifestyle Assessment', 'Labs & Genetics (Optional)', 'Review & Generate', 'Your Personalized Protocol'].map((step, index) => (
          <Badge key={index} variant={currentStep > index + 1 ? "default" : currentStep === index + 1 ? "secondary" : "outline"}>
            {step}
          </Badge>
        ))}
      </div>

      <Card className="border-2">
        <CardContent className="p-8">
          {currentStep === 1 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Personal Information</h2>
              <p className="text-gray-600">Basic demographics for personalized protocol development</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="patient_name">Full Name *</Label>
                  <Input
                    id="patient_name"
                    placeholder="Enter your full name"
                    autoComplete="off"
                    onChange={(e) => handleAssessmentChange('patient_name', e.target.value)}
                    value={assessment.patient_name || ''}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="age">Age *</Label>
                  <Input
                    id="age"
                    type="number"
                    placeholder="Your age"
                    value={assessment.age}
                    onChange={(e) => handleAssessmentChange('age', e.target.value)}
                    aria-label="Enter your age in years"
                    aria-describedby="age-description"
                  />
                  <span id="age-description" className="sr-only">Please enter your age in years</span>
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="gender">Gender *</Label>
                  <Select 
                    onValueChange={(value) => handleAssessmentChange('gender', value)} 
                    value={assessment.gender}
                    aria-label="Select your gender"
                  >
                    <SelectTrigger aria-label="Gender selection">
                      <SelectValue placeholder="Select gender" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="male">Male</SelectItem>
                      <SelectItem value="female">Female</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                      <SelectItem value="prefer_not_to_say">Prefer not to say</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Weight (lbs) *</Label>
                  <CursorPreservingInput
                    type="number"
                    placeholder="Weight in pounds"
                    onChange={(e) => handleAssessmentChange('weight', e.target.value)}
                    value={assessment.weight || ''}
                    autoComplete="off"
                  />
                </div>

                <div className="space-y-2">
                  <Label>Height *</Label>
                  <div className="flex gap-2">
                    <Select onValueChange={(value) => handleAssessmentChange('height_feet', value)} value={assessment.height_feet}>
                      <SelectTrigger>
                        <SelectValue placeholder="Feet" />
                      </SelectTrigger>
                      <SelectContent>
                        {[4,5,6,7].map(feet => (
                          <SelectItem key={feet} value={feet.toString()}>{feet} ft</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <Select onValueChange={(value) => handleAssessmentChange('height_inches', value)} value={assessment.height_inches}>
                      <SelectTrigger>
                        <SelectValue placeholder="Inches" />
                      </SelectTrigger>
                      <SelectContent>
                        {[0,1,2,3,4,5,6,7,8,9,10,11].map(inches => (
                          <SelectItem key={inches} value={inches.toString()}>{inches} in</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="space-y-2">
                  <Label htmlFor="email">Email Address *</Label>
                  <CursorPreservingInput
                    id="email"
                    type="email"
                    placeholder="your@email.com"
                    value={assessment.email}
                    onChange={(e) => handleAssessmentChange('email', e.target.value)}
                  />
                </div>
              </div>
            </div>
          )}

          {currentStep === 2 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Health Goals & Objectives</h2>
              
              <ListFieldInput
                field="primary_concerns"
                placeholder="e.g., Weight management, Low energy, Joint pain, Cognitive decline"
                label="Primary Health Concerns"
              />

              <ListFieldInput
                field="health_goals"
                placeholder="e.g., Lose 20 pounds, Increase energy, Better sleep, Anti-aging"
                label="Specific Health Goals"
              />
            </div>
          )}

          {currentStep === 3 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Medical History</h2>
              
              <ListFieldInput
                field="current_medications"
                placeholder="e.g., Metformin 500mg twice daily, Lisinopril 10mg daily"
                label="Current Medications & Supplements"
              />

              <ListFieldInput
                field="medical_history"
                placeholder="e.g., Type 2 diabetes, Hypertension, Previous injuries"
                label="Medical History & Conditions"
              />

              <ListFieldInput
                field="allergies"
                placeholder="e.g., Penicillin, Sulfa drugs, Food allergies"
                label="Known Allergies"
              />
            </div>
          )}

          {currentStep === 4 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Lifestyle Assessment</h2>
              <p className="text-gray-600">Help us understand your lifestyle for better recommendations</p>
              
              <div className="grid md:grid-cols-2 gap-6">
                <div className="space-y-2">
                  <Label>Exercise Frequency</Label>
                  <Select onValueChange={(value) => handleLifestyleFactorChange('exercise', value)} value={assessment.lifestyle_factors?.exercise}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select frequency" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="sedentary">Sedentary (little to no exercise)</SelectItem>
                      <SelectItem value="light">Light (1-2 times per week)</SelectItem>
                      <SelectItem value="moderate">Moderate (3-4 times per week)</SelectItem>
                      <SelectItem value="active">Active (5-6 times per week)</SelectItem>
                      <SelectItem value="very_active">Very Active (daily)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Sleep Quality</Label>
                  <Select onValueChange={(value) => handleLifestyleFactorChange('sleep', value)} value={assessment.lifestyle_factors?.sleep}>
                    <SelectTrigger>
                      <SelectValue placeholder="Rate your sleep" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="poor">Poor (trouble sleeping, not rested)</SelectItem>
                      <SelectItem value="fair">Fair (some sleep issues)</SelectItem>
                      <SelectItem value="good">Good (generally sleep well)</SelectItem>
                      <SelectItem value="excellent">Excellent (sleep deeply, wake refreshed)</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Stress Level</Label>
                  <Select onValueChange={(value) => handleLifestyleFactorChange('stress', value)} value={assessment.lifestyle_factors?.stress}>
                    <SelectTrigger>
                      <SelectValue placeholder="Rate your stress" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="low">Low stress</SelectItem>
                      <SelectItem value="moderate">Moderate stress</SelectItem>
                      <SelectItem value="high">High stress</SelectItem>
                      <SelectItem value="very_high">Very high stress</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-2">
                  <Label>Diet Type</Label>
                  <Select onValueChange={(value) => handleLifestyleFactorChange('diet', value)} value={assessment.lifestyle_factors?.diet}>
                    <SelectTrigger>
                      <SelectValue placeholder="Select diet type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="standard">Standard American Diet</SelectItem>
                      <SelectItem value="mediterranean">Mediterranean</SelectItem>
                      <SelectItem value="keto">Ketogenic</SelectItem>
                      <SelectItem value="paleo">Paleo</SelectItem>
                      <SelectItem value="vegetarian">Vegetarian</SelectItem>
                      <SelectItem value="vegan">Vegan</SelectItem>
                      <SelectItem value="other">Other</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
              </div>
            </div>
          )}

          {currentStep === 5 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Labs & Genetics (Optional)</h2>
              <p className="text-gray-600">Upload your lab results, genetic tests, or medical charts for comprehensive analysis</p>
              
              <Card className="p-6 border-dashed border-2 border-gray-300">
                <div className="text-center space-y-4">
                  <Upload className="h-12 w-12 text-gray-400 mx-auto" />
                  <div>
                    <h3 className="font-semibold">Upload Your Files</h3>
                    <p className="text-sm text-gray-600">Lab results, genetic tests, medical charts (PDF, images, Excel accepted)</p>
                  </div>
                  <Input
                    type="file"
                    multiple
                    accept=".pdf,.jpg,.jpeg,.png,.xlsx,.docx,.txt"
                    onChange={(e) => handleFileUpload(e.target.files)}
                    className="max-w-xs mx-auto"
                  />
                </div>
              </Card>

              {uploadedFiles.length > 0 && (
                <div className="space-y-2">
                  <h3 className="font-semibold">Uploaded Files Analysis:</h3>
                  {uploadedFiles.map((file, index) => (
                    <Alert key={index}>
                      <CheckCircle className="h-4 w-4" />
                      <AlertDescription>
                        <strong>{file.filename}</strong>: {file.analysis?.analysis_type || 'Analyzed successfully'}
                      </AlertDescription>
                    </Alert>
                  ))}
                </div>
              )}
            </div>
          )}

          {currentStep === 6 && (
            <div className="space-y-6">
              <h2 className="text-2xl font-semibold">Review & Generate</h2>
              <p className="text-gray-600">Review your information before generating your personalized protocol</p>
              
              <div className="space-y-4">
                <div className="grid md:grid-cols-2 gap-6">
                  <Card>
                    <CardContent className="p-4">
                      <h3 className="font-semibold mb-2">Personal Information</h3>
                      <p><strong>Name:</strong> {assessment.patient_name}</p>
                      <p><strong>Age:</strong> {assessment.age}</p>
                      <p><strong>Gender:</strong> {assessment.gender}</p>
                      <p><strong>Weight:</strong> {assessment.weight} lbs</p>
                      <p><strong>Height:</strong> {assessment.height_feet}'{assessment.height_inches}"</p>
                    </CardContent>
                  </Card>

                  <Card>
                    <CardContent className="p-4">
                      <h3 className="font-semibold mb-2">Health Goals</h3>
                      <p><strong>Primary Concerns:</strong> {Array.isArray(assessment.primary_concerns) ? assessment.primary_concerns.join(', ') : assessment.primary_concerns || 'None specified'}</p>
                      <p><strong>Goals:</strong> {Array.isArray(assessment.health_goals) ? assessment.health_goals.join(', ') : assessment.health_goals || 'None specified'}</p>
                    </CardContent>
                  </Card>
                </div>

                <Button 
                  onClick={generateFunctionalProtocol}
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 py-4"
                >
                  {loading ? (
                    <div className="flex items-center gap-2">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      {protocolProgress || "Generating Your Personalized Protocol..."}
                    </div>
                  ) : (
                    <div className="flex items-center gap-2">
                      <Zap className="h-5 w-5" />
                      Generate Personalized Protocol
                    </div>
                  )}
                </Button>
              </div>
            </div>
          )}

          {/* Navigation Buttons */}
          <div className="flex justify-between pt-8">
            <Button 
              variant="outline" 
              onClick={() => setCurrentStep(Math.max(1, currentStep - 1))}
              disabled={currentStep === 1 || loading}
              aria-label={`Go to previous step ${currentStep - 1 > 0 ? currentStep - 1 : ''}`}
              aria-describedby="nav-help"
            >
              Previous
            </Button>
            <Button 
              className="px-8"
              onClick={() => {
                if (currentStep < 6) {
                  console.log('Current step:', currentStep, 'Assessment data:', assessment);
                  
                  // Collect data from refs for Step 1 (Personal Information)
                  let updatedAssessment = { ...assessment };
                  if (currentStep === 1) {
                    updatedAssessment = {
                      ...assessment,
                      patient_name: fullNameRef.current?.value || '',
                      weight: weightRef.current?.value || ''
                    };
                    setAssessment(updatedAssessment);
                    console.log('Collected data from refs:', {
                      patient_name: fullNameRef.current?.value,
                      weight: weightRef.current?.value
                    });
                  }
                  
                  // Advance to next step
                  setCurrentStep(currentStep + 1);
                  
                  // Save in background (don't block progression)
                  saveAssessmentStep(currentStep, updatedAssessment).catch(error => {
                    console.error('Background save error:', error);
                  });
                }
              }}
              disabled={currentStep === 6 || loading}
              aria-label={`Proceed to ${currentStep < 6 ? `step ${currentStep + 1}` : 'generate protocol'}`}
              aria-describedby="nav-help"
            >
              Next
            </Button>
            <span id="nav-help" className="sr-only">Use Previous and Next buttons to navigate through the assessment steps</span>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const DrPeptideChat = () => (
    <div className="max-w-4xl mx-auto p-4 md:p-6">
      <Card className="h-[500px] md:h-[600px] flex flex-col">
        <CardHeader className="px-4 md:px-6">
          <CardTitle className="flex items-center gap-2">
            <div className="flex items-center gap-3">
              <div className="relative">
                <Brain className="h-6 w-6 md:h-8 md:w-8 text-blue-600" />
                <div className="absolute -top-1 -right-1 bg-green-400 rounded-full p-1">
                  <Stethoscope className="h-3 w-3 md:h-4 md:w-4 text-white" />
                </div>
              </div>
              <div>
                <h1 className="text-lg md:text-xl font-bold">Dr. Peptide AI</h1>
                <p className="text-xs md:text-sm text-gray-600">Your Functional Medicine Expert</p>
              </div>
            </div>
          </CardTitle>
        </CardHeader>
        
        <CardContent className="flex-1 flex flex-col">
          {/* Chat Messages */}
          <div className="flex-1 overflow-y-auto space-y-4 mb-4 p-4 border rounded-lg bg-gray-50">
            {chatMessages.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                <Brain className="h-12 w-12 mx-auto mb-4 text-blue-400" />
                <p>👋 Hello! I'm Dr. Peptide, your functional medicine expert.</p>
                <p className="text-sm mt-2">I can help you with peptide protocols, lab interpretation, and personalized health optimization.</p>
              </div>
            )}
            
            {chatMessages.map((message, index) => (
              <div key={index} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                <div className={`max-w-[80%] p-3 rounded-lg ${
                  message.role === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-white border shadow-sm'
                }`}>
                  {message.role === 'assistant' && (
                    <div className="flex items-center gap-2 mb-2">
                      <Brain className="h-4 w-4 text-blue-600" />
                      <span className="text-sm font-semibold text-blue-600">Dr. Peptide</span>
                    </div>
                  )}
                  <div className="whitespace-pre-wrap">{message.content}</div>
                </div>
              </div>
            ))}
            
            {chatLoading && (
              <div className="flex justify-start">
                <div className="bg-white border shadow-sm p-3 rounded-lg">
                  <div className="flex items-center gap-2">
                    <Brain className="h-4 w-4 text-blue-600" />
                    <span className="text-sm">Dr. Peptide is thinking...</span>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
                  </div>
                </div>
              </div>
            )}
          </div>
          
          {/* Chat Input */}
          <div className="flex gap-2">
            <Input
              ref={chatInputRef}
              placeholder="Ask Dr. Peptide about peptides, labs, protocols, or health optimization..."
              autoComplete="off"
              disabled={chatLoading}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !chatLoading) {
                  e.preventDefault();
                  const inputValue = chatInputRef.current?.value?.trim();
                  if (inputValue) {
                    chatWithDrPeptide(inputValue);
                    chatInputRef.current.value = '';
                  }
                }
              }}
            />
            <Button 
              onClick={() => {
                const inputValue = chatInputRef.current?.value?.trim();
                if (inputValue) {
                  chatWithDrPeptide(inputValue);
                  chatInputRef.current.value = '';
                }
              }}
              disabled={chatLoading}
            >
              <MessageCircle className="h-4 w-4" />
            </Button>
          </div>
          
          <div className="text-xs text-gray-500 mt-2 text-center">
            Dr. Peptide provides educational information. Always consult with a healthcare provider for medical decisions.
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const ProtocolLibrary = () => {
    const [protocols, setProtocols] = useState([]);
    const [filteredProtocols, setFilteredProtocols] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchQuery, setSearchQuery] = useState('');
    const [selectedCategory, setSelectedCategory] = useState('all');
    const [selectedTags, setSelectedTags] = useState([]);
    const [availableCategories, setAvailableCategories] = useState([]);
    const [availableTags, setAvailableTags] = useState([]);
    const [libraryStats, setLibraryStats] = useState(null);
    const [selectedProtocol, setSelectedProtocol] = useState(null);
    const [sortBy, setSortBy] = useState('name');
    const [viewMode, setViewMode] = useState('grid'); // grid or list
    
    // Load protocols and metadata
    useEffect(() => {
      loadProtocolLibrary();
    }, []);

    // Filter protocols when search/filter changes
    useEffect(() => {
      filterProtocols();
    }, [protocols, searchQuery, selectedCategory, selectedTags, sortBy]);

    const loadProtocolLibrary = async () => {
      try {
        setLoading(true);
        
        // Load protocols, categories, tags, and stats in parallel
        const [protocolsRes, categoriesRes, tagsRes, statsRes] = await Promise.all([
          axios.get(`${API}/protocols/library/search?limit=100`),
          axios.get(`${API}/protocols/library/categories`),
          axios.get(`${API}/protocols/library/tags`),
          axios.get(`${API}/protocols/library/stats`)
        ]);
        
        setProtocols(protocolsRes.data.protocols || []);
        setFilteredProtocols(protocolsRes.data.protocols || []);
        setAvailableCategories(categoriesRes.data.categories || []);
        setAvailableTags(tagsRes.data.tags || []);
        setLibraryStats(statsRes.data.library_stats || null);
        
      } catch (error) {
        console.error('Error loading protocol library:', error);
      } finally {
        setLoading(false);
      }
    };

    const filterProtocols = async () => {
      if (protocols.length === 0) return;
      
      try {
        // If we have active search/filters, use the search API
        if (searchQuery || selectedCategory !== 'all' || selectedTags.length > 0) {
          const params = new URLSearchParams();
          if (searchQuery) params.append('query', searchQuery);
          if (selectedCategory !== 'all') params.append('category', selectedCategory);
          if (selectedTags.length > 0) params.append('tags', selectedTags.join(','));
          params.append('limit', '100');
          
          const response = await axios.get(`${API}/protocols/library/search?${params}`);
          let filtered = response.data.protocols || [];
          
          // Apply client-side sorting
          filtered = filtered.sort((a, b) => {
            switch (sortBy) {
              case 'name':
                return (a.name || '').localeCompare(b.name || '');
              case 'category':
                return (a.category || '').localeCompare(b.category || '');
              case 'rating':
                return (b.outcome_stats?.efficacy_rating || 0) - (a.outcome_stats?.efficacy_rating || 0);
              case 'updated':
                return new Date(b.last_updated || 0) - new Date(a.last_updated || 0);
              default:
                return 0;
            }
          });
          
          setFilteredProtocols(filtered);
        } else {
          // No filters, show all protocols
          setFilteredProtocols(protocols);
        }
      } catch (error) {
        console.error('Error filtering protocols:', error);
        // Fallback to client-side filtering
        setFilteredProtocols(protocols);
      }
    };

    const toggleTag = (tag) => {
      setSelectedTags(prev => 
        prev.includes(tag) 
          ? prev.filter(t => t !== tag)
          : [...prev, tag]
      );
    };

    const downloadProtocolPDF = async (protocol) => {
      try {
        const response = await axios.get(`${API}/protocols/${protocol.id}/pdf`, {
          responseType: 'blob'
        });
        
        // Create blob link to download
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `${protocol.name.replace(/\s+/g, '_')}_Protocol.pdf`);
        document.body.appendChild(link);
        link.click();
        link.remove();
      } catch (error) {
        console.error('Error downloading PDF:', error);
      }
    };

    const ProtocolCard = ({ protocol }) => (
      <Card className="hover:shadow-lg transition-all duration-300 cursor-pointer group" 
            onClick={() => setSelectedProtocol(protocol)}>
        <CardHeader className="pb-3">
          <div className="flex justify-between items-start">
            <CardTitle className="text-lg group-hover:text-blue-600 transition-colors">
              {protocol.name}
            </CardTitle>
            <div className="flex flex-col items-end gap-1">
              <Badge variant="outline" className="text-xs">
                {protocol.category}
              </Badge>
              {protocol.outcome_stats && (
                <div className="flex items-center gap-1">
                  <Star className="h-3 w-3 text-yellow-500 fill-current" />
                  <span className="text-xs text-gray-600">
                    {protocol.outcome_stats.efficacy_rating?.toFixed(1)}
                  </span>
                </div>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-gray-600 line-clamp-3">
            {protocol.description || 'No description available'}
          </p>
          
          {/* Clinical Indications */}
          {protocol.clinical_indications && protocol.clinical_indications.length > 0 && (
            <div>
              <h4 className="font-semibold text-sm mb-2">Indications:</h4>
              <div className="flex flex-wrap gap-1">
                {protocol.clinical_indications.slice(0, 3).map((indication, idx) => (
                  <Badge key={idx} variant="secondary" className="text-xs">
                    {indication}
                  </Badge>
                ))}
                {protocol.clinical_indications.length > 3 && (
                  <Badge variant="secondary" className="text-xs">
                    +{protocol.clinical_indications.length - 3} more
                  </Badge>
                )}
              </div>
            </div>
          )}
          
          {/* Tags */}
          {protocol.tags && protocol.tags.length > 0 && (
            <div className="flex flex-wrap gap-1">
              {protocol.tags.slice(0, 4).map((tag, idx) => (
                <Badge key={idx} variant="outline" className="text-xs">
                  {tag}
                </Badge>
              ))}
            </div>
          )}
          
          {/* Action Buttons */}
          <div className="flex gap-2 pt-2">
            <Button size="sm" className="flex-1">
              View Details
            </Button>
            <Button 
              size="sm" 
              variant="outline" 
              onClick={(e) => {
                e.stopPropagation();
                downloadProtocolPDF(protocol);
              }}
            >
              <Download className="h-4 w-4" />
            </Button>
          </div>
          
          {/* Last Updated */}
          {protocol.last_updated && (
            <div className="flex items-center gap-1 text-xs text-gray-500 pt-2 border-t">
              <Clock className="h-3 w-3" />
              Updated {new Date(protocol.last_updated).toLocaleDateString()}
            </div>
          )}
        </CardContent>
      </Card>
    );

    if (loading) {
      return (
        <div className="max-w-6xl mx-auto p-4 md:p-6 space-y-8">
          <div className="text-center">
            <h1 className="text-2xl md:text-4xl font-bold">Clinical Protocol Library</h1>
            <p className="text-base md:text-lg text-gray-600 mt-2">Loading comprehensive protocols...</p>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <Card key={i} className="animate-pulse">
                <CardHeader>
                  <div className="h-6 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/2"></div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="h-4 bg-gray-200 rounded"></div>
                    <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                    <div className="h-8 bg-gray-200 rounded w-full"></div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      );
    }

    return (
      <div className="max-w-6xl mx-auto p-4 md:p-6 space-y-6 md:space-y-8">
        {/* Header with Stats */}
        <div className="text-center space-y-4">
          <h1 className="text-2xl md:text-4xl font-bold">Clinical Protocol Library</h1>
          <p className="text-base md:text-lg text-gray-600">
            Browse our comprehensive collection of evidence-based peptide therapy protocols
          </p>
          {libraryStats && (
            <div className="flex justify-center gap-6 text-sm text-gray-600">
              <div className="flex items-center gap-1">
                <FileText className="h-4 w-4" />
                {libraryStats.total_protocols} Protocols
              </div>
              <div className="flex items-center gap-1">
                <Filter className="h-4 w-4" />
                {libraryStats.categories} Categories
              </div>
              <div className="flex items-center gap-1">
                <Star className="h-4 w-4 text-yellow-500" />
                {libraryStats.average_rating?.toFixed(1)} Avg Rating
              </div>
            </div>
          )}
        </div>

        {/* Search and Filters */}
        <div className="space-y-4">
          {/* Main Search Bar */}
          <div className="flex flex-col md:flex-row gap-4">
            <div className="relative flex-1">
              <Search className="h-5 w-5 absolute left-3 top-3 text-gray-400" />
              <Input
                placeholder="Search protocols by name, indication, or mechanism..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            <div className="flex gap-2">
              <Select onValueChange={setSelectedCategory} value={selectedCategory}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="All Categories" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">All Categories</SelectItem>
                  {availableCategories.map(category => (
                    <SelectItem key={category} value={category}>
                      {category}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Select onValueChange={setSortBy} value={sortBy}>
                <SelectTrigger className="w-32">
                  <SelectValue placeholder="Sort by" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="name">Name</SelectItem>
                  <SelectItem value="category">Category</SelectItem>
                  <SelectItem value="rating">Rating</SelectItem>
                  <SelectItem value="updated">Updated</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>

          {/* Tag Filters */}
          {availableTags.length > 0 && (
            <div>
              <h3 className="text-sm font-semibold mb-2">Filter by Tags:</h3>
              <div className="flex flex-wrap gap-2">
                {availableTags.slice(0, 12).map(tag => (
                  <Badge
                    key={tag}
                    variant={selectedTags.includes(tag) ? "default" : "outline"}
                    className="cursor-pointer hover:bg-blue-100"
                    onClick={() => toggleTag(tag)}
                  >
                    {tag}
                  </Badge>
                ))}
              </div>
            </div>
          )}

          {/* Active Filters Display */}
          {(selectedCategory !== 'all' || selectedTags.length > 0 || searchQuery) && (
            <div className="flex items-center gap-2 text-sm">
              <span className="text-gray-600">Active filters:</span>
              {searchQuery && (
                <Badge variant="secondary">
                  Search: "{searchQuery}"
                  <button 
                    className="ml-1 hover:text-red-600"
                    onClick={() => setSearchQuery('')}
                  >
                    ×
                  </button>
                </Badge>
              )}
              {selectedCategory !== 'all' && (
                <Badge variant="secondary">
                  Category: {selectedCategory}
                  <button 
                    className="ml-1 hover:text-red-600"
                    onClick={() => setSelectedCategory('all')}
                  >
                    ×
                  </button>
                </Badge>
              )}
              {selectedTags.map(tag => (
                <Badge key={tag} variant="secondary">
                  {tag}
                  <button 
                    className="ml-1 hover:text-red-600"
                    onClick={() => toggleTag(tag)}
                  >
                    ×
                  </button>
                </Badge>
              ))}
            </div>
          )}
        </div>

        {/* Results Summary */}
        <div className="flex justify-between items-center">
          <p className="text-gray-600">
            Showing {filteredProtocols.length} of {protocols.length} protocols
          </p>
          <div className="flex gap-2">
            <Button
              variant={viewMode === 'grid' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('grid')}
            >
              Grid
            </Button>
            <Button
              variant={viewMode === 'list' ? 'default' : 'outline'}
              size="sm"
              onClick={() => setViewMode('list')}
            >
              List
            </Button>
          </div>
        </div>

        {/* Protocol Grid/List */}
        {filteredProtocols.length > 0 ? (
          <div className={
            viewMode === 'grid' 
              ? "grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6"
              : "space-y-4"
          }>
            {filteredProtocols.map((protocol) => (
              <ProtocolCard key={protocol.id} protocol={protocol} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12">
            <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-600 mb-2">No protocols found</h3>
            <p className="text-gray-500 mb-4">
              Try adjusting your search criteria or filters
            </p>
            <Button 
              variant="outline" 
              onClick={() => {
                setSearchQuery('');
                setSelectedCategory('all');
                setSelectedTags([]);
              }}
            >
              Clear All Filters
            </Button>
          </div>
        )}

        {/* Detailed Protocol Modal */}
        {selectedProtocol && (
          <ProtocolDetailModal 
            protocol={selectedProtocol} 
            onClose={() => setSelectedProtocol(null)}
            onDownloadPDF={downloadProtocolPDF}
          />
        )}
      </div>
    );
  };

  const ProtocolDetailModal = ({ protocol, onClose, onDownloadPDF }) => (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50" onClick={onClose}>
      <Card className="max-w-6xl w-full max-h-[90vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
        <CardHeader className="sticky top-0 bg-white border-b z-10">
          <div className="flex justify-between items-start">
            <div className="flex-1">
              <CardTitle className="text-3xl">{protocol.name}</CardTitle>
              <div className="flex items-center gap-3 mt-2">
                <Badge variant="default">{protocol.category}</Badge>
                {protocol.outcome_stats && (
                  <div className="flex items-center gap-1">
                    <Star className="h-4 w-4 text-yellow-500 fill-current" />
                    <span className="text-sm font-medium">
                      {protocol.outcome_stats.efficacy_rating?.toFixed(1)} / 5.0
                    </span>
                    <span className="text-xs text-gray-500">
                      ({protocol.outcome_stats.total_reviews} reviews)
                    </span>
                  </div>
                )}
              </div>
            </div>
            <Button variant="ghost" onClick={onClose} size="sm">
              <XCircle className="h-5 w-5" />
            </Button>
          </div>
        </CardHeader>
        
        <CardContent className="p-6 space-y-8">
          {/* Protocol Overview */}
          <section>
            <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
              <FileText className="h-5 w-5 text-blue-600" />
              Protocol Overview
            </h3>
            <div className="grid md:grid-cols-2 gap-6">
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-gray-700 mb-1">Description</h4>
                  <p className="text-gray-600">{protocol.description || 'No description available'}</p>
                </div>
                {protocol.sequence && (
                  <div>
                    <h4 className="font-semibold text-gray-700 mb-1">Peptide Sequence</h4>
                    <p className="font-mono text-sm bg-gray-50 p-2 rounded">{protocol.sequence}</p>
                  </div>
                )}
                {protocol.molecular_weight && (
                  <div>
                    <h4 className="font-semibold text-gray-700 mb-1">Molecular Weight</h4>
                    <p className="text-gray-600">{protocol.molecular_weight} Da</p>
                  </div>
                )}
              </div>
              <div className="space-y-4">
                {protocol.aliases && protocol.aliases.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-700 mb-1">Also Known As</h4>
                    <div className="flex flex-wrap gap-1">
                      {protocol.aliases.map((alias, idx) => (
                        <Badge key={idx} variant="outline" className="text-xs">
                          {alias}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
                {protocol.tags && protocol.tags.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-gray-700 mb-1">Tags</h4>
                    <div className="flex flex-wrap gap-1">
                      {protocol.tags.map((tag, idx) => (
                        <Badge key={idx} variant="secondary" className="text-xs">
                          {tag}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          </section>

          {/* Clinical Indications */}
          {protocol.clinical_indications && protocol.clinical_indications.length > 0 && (
            <section>
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Activity className="h-5 w-5 text-green-600" />
                Clinical Indications
              </h3>
              <div className="grid md:grid-cols-2 gap-2">
                {protocol.clinical_indications.map((indication, idx) => (
                  <div key={idx} className="flex items-start gap-2 p-3 bg-green-50 rounded-lg">
                    <CheckCircle className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span className="text-sm">{indication}</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Mechanism of Action */}
          {protocol.mechanism_of_action && (
            <section>
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Zap className="h-5 w-5 text-purple-600" />
                Mechanism of Action
              </h3>
              <div className="bg-purple-50 p-4 rounded-lg">
                <p className="text-gray-700 leading-relaxed">{protocol.mechanism_of_action}</p>
              </div>
            </section>
          )}

          {/* Dosing Protocols */}
          {protocol.complete_dosing_schedule && (
            <section>
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <FlaskConical className="h-5 w-5 text-orange-600" />
                Dosing Protocols
              </h3>
              <div className="bg-orange-50 p-4 rounded-lg">
                {typeof protocol.complete_dosing_schedule === 'object' ? (
                  <div className="space-y-3">
                    {Object.entries(protocol.complete_dosing_schedule).map(([key, value]) => (
                      <div key={key} className="flex justify-between items-start border-b border-orange-200 pb-2 last:border-b-0">
                        <span className="font-semibold text-orange-800 capitalize">
                          {key.replace(/_/g, ' ')}:
                        </span>
                        <span className="text-gray-700 text-right flex-1 ml-4">{value}</span>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-gray-700">{protocol.complete_dosing_schedule}</p>
                )}
              </div>
            </section>
          )}

          {/* Administration Guidelines */}
          {protocol.administration_techniques && (
            <section>
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <User className="h-5 w-5 text-blue-600" />
                Administration Guidelines
              </h3>
              <div className="bg-blue-50 p-4 rounded-lg space-y-3">
                {Object.entries(protocol.administration_techniques).map(([key, value]) => (
                  <div key={key}>
                    <h4 className="font-semibold text-blue-800 capitalize mb-1">
                      {key.replace(/_/g, ' ')}
                    </h4>
                    <p className="text-gray-700">
                      {Array.isArray(value) ? value.join(', ') : value}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Safety Profile */}
          {(protocol.safety_profile || protocol.contraindications) && (
            <section>
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Shield className="h-5 w-5 text-red-600" />
                Safety Profile & Contraindications
              </h3>
              <div className="bg-red-50 p-4 rounded-lg space-y-4">
                {protocol.safety_profile?.common_side_effects && (
                  <div>
                    <h4 className="font-semibold text-red-800 mb-2">Common Side Effects</h4>
                    <div className="space-y-2">
                      {protocol.safety_profile.common_side_effects.map((effect, idx) => (
                        <div key={idx} className="flex justify-between items-center">
                          <span className="text-gray-700">
                            {typeof effect === 'object' ? effect.effect : effect}
                          </span>
                          {typeof effect === 'object' && effect.frequency && (
                            <Badge variant="outline" className="text-xs">
                              {effect.frequency}
                            </Badge>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                
                {protocol.contraindications && protocol.contraindications.length > 0 && (
                  <div>
                    <h4 className="font-semibold text-red-800 mb-2">Contraindications</h4>
                    <ul className="space-y-1">
                      {protocol.contraindications.map((contra, idx) => (
                        <li key={idx} className="flex items-start gap-2">
                          <AlertTriangle className="h-4 w-4 text-red-600 mt-0.5 flex-shrink-0" />
                          <span className="text-gray-700">{contra}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </section>
          )}

          {/* Monitoring Requirements */}
          {protocol.monitoring_requirements && (
            <section>
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <Eye className="h-5 w-5 text-indigo-600" />
                Monitoring Requirements
              </h3>
              <div className="bg-indigo-50 p-4 rounded-lg space-y-3">
                {Object.entries(protocol.monitoring_requirements).map(([key, value]) => (
                  <div key={key}>
                    <h4 className="font-semibold text-indigo-800 capitalize mb-1">
                      {key.replace(/_/g, ' ')}
                    </h4>
                    <p className="text-gray-700">
                      {Array.isArray(value) ? value.join(', ') : value}
                    </p>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* References */}
          {protocol.references && protocol.references.length > 0 && (
            <section>
              <h3 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <BookOpen className="h-5 w-5 text-gray-600" />
                Clinical References
              </h3>
              <div className="space-y-2">
                {protocol.references.map((ref, idx) => (
                  <div key={idx} className="p-3 bg-gray-50 rounded-lg">
                    <span className="text-sm text-gray-700">{idx + 1}. {ref}</span>
                  </div>
                ))}
              </div>
            </section>
          )}

          {/* Action Buttons */}
          <section className="border-t pt-6">
            <div className="flex flex-col sm:flex-row gap-4">
              <Button 
                className="flex-1"
                onClick={() => {
                  // Generate personalized protocol
                  generateFunctionalProtocol();
                  onClose();
                }}
              >
                <Zap className="h-4 w-4 mr-2" />
                Generate Personalized Protocol
              </Button>
              <Button 
                variant="outline" 
                onClick={() => onDownloadPDF(protocol)}
                className="sm:w-auto"
              >
                <Download className="h-4 w-4 mr-2" />
                Download PDF
              </Button>
              <Button 
                variant="outline"
                onClick={() => {
                  setCurrentView('chat');
                  onClose();
                }}
                className="sm:w-auto"
              >
                <MessageCircle className="h-4 w-4 mr-2" />
                Ask Dr. Peptide
              </Button>
            </div>
          </section>

          {/* Last Updated */}
          {protocol.last_updated && (
            <div className="text-xs text-gray-500 text-center pt-4 border-t">
              Last updated: {new Date(protocol.last_updated).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );

  const PeptidesView = () => {
    const [selectedPeptideForView, setSelectedPeptideForView] = useState(null);
    const [filteredPeptides, setFilteredPeptides] = useState([]);
    const [categoryFilter, setCategoryFilter] = useState('all');
    const [searchQuery, setSearchQuery] = useState('');
    const [sortBy, setSortBy] = useState('name');
    const [showAdvancedFilters, setShowAdvancedFilters] = useState(false);
    const [showSavedFilters, setShowSavedFilters] = useState(false);
    const [evidenceFilter, setEvidenceFilter] = useState('');
    const [routeFilter, setRouteFilter] = useState('');
    const [regulatoryFilter, setRegulatoryFilter] = useState('');

    // Progress Dashboard State
    const [progressData, setProgressData] = useState(null);
    const [loadingProgress, setLoadingProgress] = useState(false);
    const [selectedTimeframe, setSelectedTimeframe] = useState('3months');
    const [selectedMetrics, setSelectedMetrics] = useState(['energy_levels', 'sleep_quality', 'weight']);

    useEffect(() => {
      // Ensure peptidesDatabase is available and is an array
      if (!peptidesDatabase || !Array.isArray(peptidesDatabase) || peptidesDatabase.length === 0) {
        setFilteredPeptides([]);
        return;
      }

      let filtered = [...peptidesDatabase]; // Create a copy to avoid mutation

      // Category filter
      if (categoryFilter && categoryFilter !== 'all' && categoryFilter !== '') {
        filtered = filtered.filter(peptide => peptide.category === categoryFilter);
      }

      // Search filter
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        filtered = filtered.filter(peptide =>
          (peptide.name && peptide.name.toLowerCase().includes(query)) ||
          (peptide.mechanism_of_action && peptide.mechanism_of_action.toLowerCase().includes(query)) ||
          (peptide.indications && Array.isArray(peptide.indications) && 
           peptide.indications.some(indication => indication.toLowerCase().includes(query)))
        );
      }

      // Evidence level filter
      if (evidenceFilter) {
        filtered = filtered.filter(peptide => 
          peptide.evidence_level && peptide.evidence_level.includes(evidenceFilter)
        );
      }

      // Administration route filter
      if (routeFilter) {
        filtered = filtered.filter(peptide => 
          peptide.administration_techniques && 
          JSON.stringify(peptide.administration_techniques).toLowerCase().includes(routeFilter)
        );
      }

      // Regulatory status filter
      if (regulatoryFilter) {
        filtered = filtered.filter(peptide => 
          peptide.regulatory_status && 
          peptide.regulatory_status.toLowerCase().includes(regulatoryFilter.toLowerCase())
        );
      }

      // Sorting
      filtered.sort((a, b) => {
        switch (sortBy) {
          case 'category':
            return (a.category || '').localeCompare(b.category || '');
          case 'evidence':
            const evidenceOrder = { 'Level 1A': 5, 'Level 1B': 4, 'Level 2A': 3, 'Level 2B': 2, 'Level 3': 1 };
            const aEvidence = a.evidence_level ? evidenceOrder[a.evidence_level.split(' ')[0] + ' ' + a.evidence_level.split(' ')[1]] || 0 : 0;
            const bEvidence = b.evidence_level ? evidenceOrder[b.evidence_level.split(' ')[0] + ' ' + b.evidence_level.split(' ')[1]] || 0 : 0;
            return bEvidence - aEvidence; // Higher evidence first
          case 'newest':
            // For now, reverse alphabetical (would need actual date field)
            return (b.name || '').localeCompare(a.name || '');
          default:
            return (a.name || '').localeCompare(b.name || '');
        }
      });
      
      setFilteredPeptides(filtered);
    }, [peptidesDatabase, categoryFilter, searchQuery, evidenceFilter, routeFilter, regulatoryFilter, sortBy]);

    const PeptideCard = ({ peptide }) => {
      // Safely handle missing data
      const indications = peptide.indications || [];
      const mechanismText = peptide.mechanism_of_action || 'No mechanism information available';
      
      return (
        <Card className="hover:shadow-md transition-shadow cursor-pointer" 
              onClick={() => setSelectedPeptideForView(peptide)}>
          <CardHeader className="pb-2">
            <div className="flex justify-between items-start">
              <CardTitle className="text-lg">{peptide.name || 'Unknown Peptide'}</CardTitle>
              <Badge variant="outline" className="ml-2">{peptide.category || 'Uncategorized'}</Badge>
            </div>
            {peptide.evidence_level && (
              <Badge variant="secondary" className="w-fit text-xs">
                {peptide.evidence_level.split('.')[0]}
              </Badge>
            )}
          </CardHeader>
          <CardContent className="space-y-3">
            <div>
              <h4 className="font-semibold text-sm mb-1">Indications:</h4>
              <div className="flex flex-wrap gap-1">
                {indications.length > 0 ? (
                  <>
                    {indications.slice(0, 3).map((indication, idx) => (
                      <Badge key={idx} variant="outline" className="text-xs">
                        {indication}
                      </Badge>
                    ))}
                    {indications.length > 3 && (
                      <Badge variant="outline" className="text-xs">
                        +{indications.length - 3} more
                      </Badge>
                    )}
                  </>
                ) : (
                  <Badge variant="outline" className="text-xs text-gray-500">
                    No indications listed
                  </Badge>
                )}
              </div>
            </div>
            
            <div>
              <h4 className="font-semibold text-sm mb-1">Mechanism of Action:</h4>
              <p className="text-sm text-gray-600 line-clamp-2">
                {mechanismText.length > 120 ? mechanismText.substring(0, 120) + '...' : mechanismText}
              </p>
            </div>
            
            {peptide.regulatory_status && (
              <div className="flex items-center gap-2">
                <Shield className="h-4 w-4 text-green-600" />
                <span className="text-xs text-green-600 font-medium">
                  {peptide.regulatory_status}
                </span>
              </div>
            )}
          </CardContent>
        </Card>
      );
    };

    const PeptideDetailModal = ({ peptide, onClose }) => {
      // Safely handle missing data
      const indications = peptide.indications || [];
      const mechanismText = peptide.mechanism_of_action || 'No mechanism information available';
      
      return (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-4xl w-full max-h-[90vh] overflow-y-auto">
            <div className="sticky top-0 bg-white border-b p-6 flex justify-between items-center">
              <div>
                <h1 className="text-2xl font-bold">{peptide.name || 'Unknown Peptide'}</h1>
                <div className="flex gap-2 mt-2">
                  <Badge>{peptide.category || 'Uncategorized'}</Badge>
                  {peptide.regulatory_status && (
                    <Badge variant="secondary">{peptide.regulatory_status}</Badge>
                  )}
                </div>
              </div>
              <Button variant="ghost" onClick={onClose} size="sm">
                <XCircle className="h-5 w-5" />
              </Button>
            </div>
            
            <div className="p-6 space-y-6">
              {/* Indications */}
              <section>
                <h3 className="text-lg font-semibold mb-2 text-blue-800">Clinical Indications</h3>
                <div className="flex flex-wrap gap-2">
                  {indications.length > 0 ? (
                    indications.map((indication, idx) => (
                      <Badge key={idx} variant="outline">{indication}</Badge>
                    ))
                  ) : (
                    <Badge variant="outline" className="text-gray-500">No indications listed</Badge>
                  )}
                </div>
              </section>

              {/* Mechanism of Action */}
              <section>
                <h3 className="text-lg font-semibold mb-2 text-blue-800">Mechanism of Action</h3>
                <p className="text-gray-700">{mechanismText}</p>
              </section>

              {/* Evidence Level */}
              {peptide.evidence_level && (
                <section>
                  <h3 className="text-lg font-semibold mb-2 text-blue-800">Evidence Level</h3>
                  <Card className="bg-green-50 border-green-200">
                    <CardContent className="p-4">
                      <p className="text-green-800">{peptide.evidence_level}</p>
                    </CardContent>
                  </Card>
                </section>
              )}

              {/* Complete Dosing Schedule */}
              {peptide.complete_dosing_schedule && (
                <section>
                  <details className="group">
                    <summary className="text-lg font-semibold mb-2 text-blue-800 cursor-pointer hover:text-blue-600">
                      Complete Dosing Schedule
                    </summary>
                    <Card className="mt-2">
                      <CardContent className="p-4 space-y-2">
                        {typeof peptide.complete_dosing_schedule === 'object' && peptide.complete_dosing_schedule !== null ? (
                          Object.entries(peptide.complete_dosing_schedule).map(([key, value]) => (
                            <div key={key} className="flex justify-between">
                              <span className="font-medium capitalize">{key.replace('_', ' ')}:</span>
                              <span className="text-gray-700">{value}</span>
                            </div>
                          ))
                        ) : (
                          <p className="text-gray-700">{peptide.complete_dosing_schedule}</p>
                        )}
                      </CardContent>
                    </Card>
                  </details>
                </section>
              )}

              {/* Administration Techniques */}
              {peptide.administration_techniques && (
                <section>
                  <details className="group">
                    <summary className="text-lg font-semibold mb-2 text-blue-800 cursor-pointer hover:text-blue-600">
                      Administration Techniques
                    </summary>
                    <Card className="mt-2">
                      <CardContent className="p-4 space-y-2">
                        {typeof peptide.administration_techniques === 'object' && peptide.administration_techniques !== null ? (
                          Object.entries(peptide.administration_techniques).map(([key, value]) => (
                            <div key={key}>
                              <span className="font-medium capitalize">{key.replace('_', ' ')}:</span>
                              <p className="text-gray-700 ml-4">
                                {Array.isArray(value) ? value.join(', ') : value}
                              </p>
                            </div>
                          ))
                        ) : (
                          <p className="text-gray-700">No administration information available</p>
                        )}
                      </CardContent>
                    </Card>
                  </details>
                </section>
              )}

              {/* Safety Profile */}
              {peptide.safety_profile && (
                <section>
                  <details className="group">
                    <summary className="text-lg font-semibold mb-2 text-blue-800 cursor-pointer hover:text-blue-600">
                      Safety Profile
                    </summary>
                    <Card className="mt-2">
                      <CardContent className="p-4 space-y-4">
                        {peptide.safety_profile.contraindications && Array.isArray(peptide.safety_profile.contraindications) && (
                          <div>
                            <h4 className="font-semibold text-red-700">Contraindications:</h4>
                            <ul className="list-disc ml-4 text-red-600">
                              {peptide.safety_profile.contraindications.map((item, idx) => (
                                <li key={idx}>{item}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {peptide.safety_profile.side_effects && Array.isArray(peptide.safety_profile.side_effects) && (
                          <div>
                            <h4 className="font-semibold text-orange-700">Side Effects:</h4>
                            <ul className="list-disc ml-4 text-orange-600">
                              {peptide.safety_profile.side_effects.map((item, idx) => (
                                <li key={idx}>{item}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                        {peptide.safety_profile.monitoring_required && Array.isArray(peptide.safety_profile.monitoring_required) && (
                          <div>
                            <h4 className="font-semibold text-blue-700">Monitoring Required:</h4>
                            <ul className="list-disc ml-4 text-blue-600">
                              {peptide.safety_profile.monitoring_required.map((item, idx) => (
                                <li key={idx}>{item}</li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </CardContent>
                    </Card>
                  </details>
                </section>
              )}

              {/* Expected Timelines */}
              {peptide.expected_timelines && (
                <section>
                  <details className="group">
                    <summary className="text-lg font-semibold mb-2 text-blue-800 cursor-pointer hover:text-blue-600">
                      Expected Timelines
                    </summary>
                    <Card className="mt-2">
                      <CardContent className="p-4 space-y-2">
                        {typeof peptide.expected_timelines === 'object' && peptide.expected_timelines !== null ? (
                          Object.entries(peptide.expected_timelines).map(([key, value]) => (
                            <div key={key} className="flex justify-between">
                              <span className="font-medium capitalize">{key.replace('_', ' ')}:</span>
                              <span className="text-gray-700">{value}</span>
                            </div>
                          ))
                        ) : (
                          <p className="text-gray-700">No timeline information available</p>
                        )}
                      </CardContent>
                    </Card>
                  </details>
                </section>
              )}

              {/* Scientific References */}
              {peptide.scientific_references && Array.isArray(peptide.scientific_references) && peptide.scientific_references.length > 0 && (
                <section>
                  <details className="group">
                    <summary className="text-lg font-semibold mb-2 text-blue-800 cursor-pointer hover:text-blue-600">
                      Scientific References
                    </summary>
                    <Card className="mt-2">
                      <CardContent className="p-4">
                        <ol className="list-decimal ml-4 space-y-1">
                          {peptide.scientific_references.map((ref, idx) => (
                            <li key={idx} className="text-sm text-gray-700">{ref}</li>
                          ))}
                        </ol>
                      </CardContent>
                    </Card>
                  </details>
                </section>
              )}
            </div>
          </div>
        </div>
      );
    };

    return (
      <div className="max-w-6xl mx-auto p-6 space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold">Comprehensive Peptides Database</h1>
          <p className="text-lg text-gray-600">
            Evidence-based clinical information for {peptidesDatabase.length} therapeutic peptides
          </p>
          <p className="text-sm text-gray-500">
            Detailed protocols, dosing schedules, safety profiles, and scientific references
          </p>
        </div>

        {/* Advanced Search and Filters */}
        <div className="grid md:grid-cols-4 gap-4 mb-8">
          <div className="md:col-span-2">
            <div className="relative">
              <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search peptides by name, indications, or mechanism..."
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
              />
            </div>
          </div>
          
          <div>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <option value="">All Categories</option>
              {peptideCategories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </div>
          
          <div>
            <select
              className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="name">Sort by Name</option>
              <option value="category">Sort by Category</option>
              <option value="evidence">Sort by Evidence Level</option>
              <option value="newest">Sort by Recently Added</option>
            </select>
          </div>
        </div>

        {/* Advanced Filters Toggle */}
        <div className="mb-6">
          <Button 
            variant="outline" 
            onClick={() => setShowAdvancedFilters(!showAdvancedFilters)}
            className="mb-4"
          >
            <Filter className="h-4 w-4 mr-2" />
            {showAdvancedFilters ? 'Hide' : 'Show'} Advanced Filters
          </Button>
          
          {showAdvancedFilters && (
            <Card className="p-4">
              <div className="grid md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-1">Evidence Level</label>
                  <select
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={evidenceFilter}
                    onChange={(e) => setEvidenceFilter(e.target.value)}
                  >
                    <option value="">All Evidence Levels</option>
                    <option value="Level 1A">Level 1A - Highest</option>
                    <option value="Level 1B">Level 1B - High</option>
                    <option value="Level 2A">Level 2A - Moderate-High</option>
                    <option value="Level 2B">Level 2B - Moderate</option>
                    <option value="Level 3">Level 3 - Limited</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Administration Route</label>
                  <select
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={routeFilter}
                    onChange={(e) => setRouteFilter(e.target.value)}
                  >
                    <option value="">All Routes</option>
                    <option value="subcutaneous">Subcutaneous</option>
                    <option value="oral">Oral</option>
                    <option value="nasal">Nasal</option>
                    <option value="topical">Topical</option>
                    <option value="intravenous">IV</option>
                  </select>
                </div>
                
                <div>
                  <label className="block text-sm font-medium mb-1">Regulatory Status</label>
                  <select
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={regulatoryFilter}
                    onChange={(e) => setRegulatoryFilter(e.target.value)}
                  >
                    <option value="">All Regulatory Status</option>
                    <option value="FDA approved">FDA Approved</option>
                    <option value="investigational">Investigational</option>
                    <option value="research">Research Only</option>
                    <option value="supplement">Dietary Supplement</option>
                  </select>
                </div>
              </div>
              
              <div className="mt-4 flex gap-2">
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => {
                    setEvidenceFilter('');
                    setRouteFilter('');
                    setRegulatoryFilter('');
                    setCategoryFilter('');
                    setSearchQuery('');
                  }}
                >
                  Clear All Filters
                </Button>
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => setShowSavedFilters(!showSavedFilters)}
                >
                  Save Filter Preset
                </Button>
              </div>
            </Card>
          )}
        </div>

        <div className="flex gap-2 text-sm text-gray-600 mb-6">
          <Badge variant="outline">{filteredPeptides.length} peptides</Badge>
          <Badge variant="outline">{peptideCategories.length} categories</Badge>
        </div>

        {/* Peptides Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredPeptides.map((peptide, index) => (
            <PeptideCard key={index} peptide={peptide} />
          ))}
        </div>

        {filteredPeptides.length === 0 && peptidesDatabase.length > 0 && (
          <div className="text-center py-12">
            <FlaskConical className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-semibold text-gray-600">No peptides found</h3>
            <p className="text-gray-500">Try adjusting your search or category filter</p>
          </div>
        )}

        {/* Loading State */}
        {peptidesDatabase.length === 0 && (
          <div className="text-center py-12">
            <FlaskConical className="h-12 w-12 text-blue-600 mx-auto mb-4 animate-pulse" />
            <h3 className="text-lg font-semibold text-gray-600">Loading Peptides Database...</h3>
            <p className="text-gray-500">Please wait while we load the comprehensive peptide information</p>
          </div>
        )}

        {/* Peptide Detail Modal */}
        {selectedPeptideForView && (
          <PeptideDetailModal 
            peptide={selectedPeptideForView} 
            onClose={() => setSelectedPeptideForView(null)} 
          />
        )}
      </div>
    );
  };

  const CollectiveIntelligenceNetwork = () => (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      <div className="text-center space-y-4">
        <h1 className="text-4xl font-bold">Real-Time Collective Intelligence</h1>
        <p className="text-lg text-gray-600">Watch our network learn and improve in real-time</p>
        <p className="text-gray-500">Expert practitioners contribute their wisdom, making our AI smarter with every interaction</p>
      </div>

      {/* Network Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        <Card className="text-center p-6">
          <div className="text-3xl font-bold text-blue-600">94.2%</div>
          <div className="text-sm text-gray-600">AI Accuracy with Network Data</div>
        </Card>
        <Card className="text-center p-6">
          <div className="text-3xl font-bold text-green-600">324</div>
          <div className="text-sm text-gray-600">Training Data Points</div>
        </Card>
        <Card className="text-center p-6">
          <div className="text-3xl font-bold text-purple-600">89</div>
          <div className="text-sm text-gray-600">Practitioner Insights Integrated</div>
        </Card>
        <Card className="text-center p-6">
          <div className="text-3xl font-bold text-orange-600">156</div>
          <div className="text-sm text-gray-600">Validated Successful Outcomes</div>
        </Card>
      </div>

      {/* How It Works */}
      <Card>
        <CardHeader>
          <CardTitle>How Our Collective Intelligence Network Works</CardTitle>
          <CardDescription>Every practitioner interaction makes our AI smarter and your protocols more precise</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-3 gap-6">
            <div className="text-center space-y-4">
              <div className="bg-blue-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto">
                <Users className="h-8 w-8 text-blue-600" />
              </div>
              <h3 className="font-semibold">Expert Practitioners Contribute</h3>
              <p className="text-sm text-gray-600">12+ expert practitioners share real-world outcomes, protocol refinements, and clinical insights</p>
            </div>
            <div className="text-center space-y-4">
              <div className="bg-green-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto">
                <Brain className="h-8 w-8 text-green-600" />
              </div>
              <h3 className="font-semibold">AI Learns & Adapts</h3>
              <p className="text-sm text-gray-600">Our AI integrates practitioner wisdom with clinical evidence to continuously improve recommendations</p>
            </div>
            <div className="text-center space-y-4">
              <div className="bg-purple-100 rounded-full w-16 h-16 flex items-center justify-center mx-auto">
                <TrendingUp className="h-8 w-8 text-purple-600" />
              </div>
              <h3 className="font-semibold">Better Outcomes for All</h3>
              <p className="text-sm text-gray-600">Every patient benefits from the collective knowledge of our entire practitioner network</p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recent Network Activity */}
      <Card>
        <CardHeader>
          <CardTitle>Recent Network Contributions</CardTitle>
          <CardDescription>Latest insights from our expert practitioner network</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[
              {
                type: "Protocol Refinement",
                doctor: "Dr. Sarah Chen",
                specialty: "Longevity",
                impact: "High Impact",
                time: "2 hours ago"
              },
              {
                type: "Outcome Report",
                doctor: "Dr. Michael Rodriguez", 
                specialty: "Athletic Performance",
                impact: "Medium Impact",
                time: "4 hours ago"
              },
              {
                type: "Evidence Submission",
                doctor: "Dr. Jennifer Kim",
                specialty: "Cognitive Enhancement", 
                impact: "High Impact",
                time: "6 hours ago"
              }
            ].map((activity, index) => (
              <div key={index} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex items-center gap-4">
                  <div className="bg-blue-100 rounded-full w-10 h-10 flex items-center justify-center">
                    {activity.doctor.split(' ').map(n => n[0]).join('')}
                  </div>
                  <div>
                    <div className="font-semibold">{activity.type}</div>
                    <div className="text-sm text-gray-600">{activity.doctor} • {activity.specialty}</div>
                  </div>
                </div>
                <div className="text-right">
                  <Badge variant={activity.impact === "High Impact" ? "default" : "secondary"}>
                    {activity.impact}
                  </Badge>
                  <div className="text-xs text-gray-500 mt-1">{activity.time}</div>
                </div>
              </div>
            ))}
          </div>
          <Button variant="outline" className="w-full mt-4">View All Network Activity</Button>
        </CardContent>
      </Card>

      {/* Expert Network by Specialty */}
      <Card>
        <CardHeader>
          <CardTitle>Expert Network by Specialty</CardTitle>
          <CardDescription>Specialized expertise across all peptide therapy areas</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
            {[
              { specialty: "Longevity & Anti-Aging", experts: 12, successRate: "94.2%" },
              { specialty: "Athletic Performance", experts: 8, successRate: "96.1%" },
              { specialty: "Cognitive Enhancement", experts: 7, successRate: "91.5%" },
              { specialty: "Recovery & Healing", experts: 9, successRate: "88.9%" },
              { specialty: "Metabolic Optimization", experts: 6, successRate: "92.3%" },
              { specialty: "Sexual Wellness", experts: 5, successRate: "89.7%" }
            ].map((area, index) => (
              <Card key={index} className="p-4">
                <h4 className="font-semibold mb-2">{area.specialty}</h4>
                <div className="text-sm text-gray-600">
                  <div>{area.experts} expert practitioners</div>
                  <div className="font-semibold text-green-600 text-lg">{area.successRate}</div>
                  <div className="text-xs">Success Rate</div>
                </div>
              </Card>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Call to Action */}
      <Card className="bg-gradient-to-r from-blue-600 to-purple-600 text-white">
        <CardContent className="p-8 text-center space-y-4">
          <h2 className="text-2xl font-bold">Join Our Expert Network</h2>
          <p>Contribute to the future of peptide medicine and help our AI learn from your clinical experience</p>
          <div className="flex gap-4 justify-center">
            <Button variant="secondary">
              <User className="h-4 w-4 mr-2" />
              Practitioner Registration
            </Button>
            <Button variant="outline" className="border-white text-white hover:bg-white hover:text-purple-600">
              <Network className="h-4 w-4 mr-2" />
              Learn More
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );

  const ProtocolView = () => {
    console.log('🔍 ProtocolView rendering, generatedProtocol:', generatedProtocol);
    
    if (!generatedProtocol) {
      return (
        <div className="max-w-4xl mx-auto p-6 text-center">
          <h2 className="text-2xl font-bold text-gray-600 mb-4">No Protocol Generated</h2>
          <p className="text-gray-500">Please complete the assessment first to generate your personalized protocol.</p>
          <Button 
            onClick={() => setCurrentView('assessment')}
            className="mt-4"
          >
            Start Assessment
          </Button>
        </div>
      );
    }

    return (
      <div className="max-w-4xl mx-auto p-6 space-y-8">
        <div className="text-center space-y-4">
          <h1 className="text-4xl font-bold text-green-600">🎉 Your Personalized Protocol</h1>
          <p className="text-lg text-gray-600">Generated by Dr. Peptide AI with functional medicine expertise</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>
              {generatedProtocol?.ai_analysis ? 
                "Your Personalized Protocol" : 
                "Protocol Generated"
              }
            </CardTitle>
            <CardDescription>
              {generatedProtocol?.clinical_reasoning || 
               generatedProtocol?.ai_analysis ||
               "Comprehensive functional medicine approach tailored for your health goals"
              }
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
              {/* Mechanism of Action */}
              {generatedProtocol.mechanism_of_action && (
                <div>
                  <h3 className="font-semibold mb-4 flex items-center gap-2">
                    <Zap className="h-5 w-5 text-blue-600" />
                    Mechanism of Action
                  </h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {generatedProtocol.mechanism_of_action.primary_mechanisms && (
                      <Card className="p-4">
                        <h4 className="font-medium mb-2">Primary Mechanisms</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {generatedProtocol.mechanism_of_action.primary_mechanisms.map((mechanism, i) => (
                            <li key={i}>• {mechanism}</li>
                          ))}
                        </ul>
                      </Card>
                    )}
                    {generatedProtocol.mechanism_of_action.molecular_targets && (
                      <Card className="p-4">
                        <h4 className="font-medium mb-2">Molecular Targets</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {generatedProtocol.mechanism_of_action.molecular_targets.map((target, i) => (
                            <li key={i}>• {target}</li>
                          ))}
                        </ul>
                      </Card>
                    )}
                  </div>
                </div>
              )}

              {/* Primary Peptides */}
              {generatedProtocol.primary_peptides && (
                <div>
                  <h3 className="font-semibold mb-4 flex items-center gap-2">
                    <Pill className="h-5 w-5 text-green-600" />
                    Primary Peptides
                  </h3>
                  <div className="grid gap-4">
                    {generatedProtocol.primary_peptides.map((peptide, index) => (
                      <Card key={index} className="p-4 bg-blue-50">
                        <div className="flex justify-between items-start mb-2">
                          <h4 className="font-semibold text-blue-800">{peptide.name}</h4>
                          <Badge>{peptide.duration}</Badge>
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{peptide.indication || peptide.rationale}</p>
                        <div className="text-sm">
                          <span className="font-medium">Dosage:</span> {peptide.dosage || peptide.personalized_dosing} • 
                          <span className="font-medium">Frequency:</span> {peptide.frequency}
                        </div>
                        <p className="text-sm text-green-700 mt-2">{peptide.expected_benefits}</p>
                      </Card>
                    ))}
                  </div>
                </div>
              )}

              {/* Detailed Dosing Protocols */}
              {generatedProtocol.detailed_dosing_protocols && (
                <div>
                  <h3 className="font-semibold mb-4 flex items-center gap-2">
                    <Calculator className="h-5 w-5 text-purple-600" />
                    Detailed Dosing Protocols
                  </h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {generatedProtocol.detailed_dosing_protocols.standard_dosing && (
                      <Card className="p-4">
                        <h4 className="font-medium mb-2">Standard Dosing</h4>
                        <div className="text-sm space-y-2">
                          {Object.entries(generatedProtocol.detailed_dosing_protocols.standard_dosing).map(([peptide, dosing]) => (
                            <div key={peptide} className="border-l-2 border-blue-300 pl-3">
                              <div className="font-medium">{peptide}</div>
                              <div className="text-gray-600">{typeof dosing === 'object' ? 
                                `${dosing.dose} ${dosing.frequency} ${dosing.route}` : 
                                dosing}
                              </div>
                            </div>
                          ))}
                        </div>
                      </Card>
                    )}
                    {generatedProtocol.detailed_dosing_protocols.injection_techniques && (
                      <Card className="p-4">
                        <h4 className="font-medium mb-2">Injection Techniques</h4>
                        <div className="text-sm text-gray-600">
                          {typeof generatedProtocol.detailed_dosing_protocols.injection_techniques === 'object' ?
                            Object.entries(generatedProtocol.detailed_dosing_protocols.injection_techniques).map(([key, value]) => (
                              <div key={key}><span className="font-medium">{key}:</span> {Array.isArray(value) ? value.join(', ') : value}</div>
                            )) :
                            generatedProtocol.detailed_dosing_protocols.injection_techniques
                          }
                        </div>
                      </Card>
                    )}
                  </div>
                </div>
              )}

              {/* Stacking Combinations */}
              {generatedProtocol.stacking_combinations && (
                <div>
                  <h3 className="font-semibold mb-4 flex items-center gap-2">
                    <Layers className="h-5 w-5 text-orange-600" />
                    Stacking Combinations
                  </h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {generatedProtocol.stacking_combinations.recommended_stacks && (
                      <Card className="p-4">
                        <h4 className="font-medium mb-2">Recommended Stacks</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {generatedProtocol.stacking_combinations.recommended_stacks.map((stack, i) => (
                            <li key={i}>• {stack}</li>
                          ))}
                        </ul>
                      </Card>
                    )}
                    {generatedProtocol.stacking_combinations.synergistic_effects && (
                      <Card className="p-4">
                        <h4 className="font-medium mb-2">Synergistic Effects</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {generatedProtocol.stacking_combinations.synergistic_effects.map((effect, i) => (
                            <li key={i}>• {effect}</li>
                          ))}
                        </ul>
                      </Card>
                    )}
                  </div>
                </div>
              )}

              {/* Comprehensive Contraindications */}
              {generatedProtocol.comprehensive_contraindications && (
                <div>
                  <h3 className="font-semibold mb-4 flex items-center gap-2">
                    <AlertTriangle className="h-5 w-5 text-red-600" />
                    Contraindications & Safety
                  </h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {generatedProtocol.comprehensive_contraindications.absolute_contraindications && (
                      <Card className="p-4 border-red-200">
                        <h4 className="font-medium mb-2 text-red-800">Absolute Contraindications</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {generatedProtocol.comprehensive_contraindications.absolute_contraindications.map((contra, i) => (
                            <li key={i}>• {contra}</li>
                          ))}
                        </ul>
                      </Card>
                    )}
                    {generatedProtocol.comprehensive_contraindications.drug_interactions && (
                      <Card className="p-4 border-yellow-200">
                        <h4 className="font-medium mb-2 text-yellow-800">Drug Interactions</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {generatedProtocol.comprehensive_contraindications.drug_interactions.map((interaction, i) => (
                            <li key={i}>• {interaction}</li>
                          ))}
                        </ul>
                      </Card>
                    )}
                  </div>
                </div>
              )}

              {/* Monitoring Requirements */}
              {generatedProtocol.monitoring_requirements && (
                <div>
                  <h3 className="font-semibold mb-4 flex items-center gap-2">
                    <Activity className="h-5 w-5 text-indigo-600" />
                    Monitoring Requirements
                  </h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {generatedProtocol.monitoring_requirements.baseline_labs && (
                      <Card className="p-4">
                        <h4 className="font-medium mb-2">Baseline Labs</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {generatedProtocol.monitoring_requirements.baseline_labs.map((lab, i) => (
                            <li key={i}>• {lab}</li>
                          ))}
                        </ul>
                      </Card>
                    )}
                    {generatedProtocol.monitoring_requirements.monitoring_schedule && (
                      <Card className="p-4">
                        <h4 className="font-medium mb-2">Monitoring Schedule</h4>
                        <div className="text-sm text-gray-600 space-y-2">
                          {Object.entries(generatedProtocol.monitoring_requirements.monitoring_schedule).map(([timepoint, tests]) => (
                            <div key={timepoint} className="border-l-2 border-indigo-300 pl-3">
                              <div className="font-medium">{timepoint}</div>
                              <div>{Array.isArray(tests) ? tests.join(', ') : tests}</div>
                            </div>
                          ))}
                        </div>
                      </Card>
                    )}
                  </div>
                </div>
              )}

              {/* Evidence-Based Support */}
              {generatedProtocol.evidence_based_support && (
                <div>
                  <h3 className="font-semibold mb-4 flex items-center gap-2">
                    <BookOpen className="h-5 w-5 text-teal-600" />
                    Evidence-Based Support
                  </h3>
                  <div className="grid md:grid-cols-2 gap-4">
                    {generatedProtocol.evidence_based_support.clinical_trials && (
                      <Card className="p-4">
                        <h4 className="font-medium mb-2">Clinical Trials</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {generatedProtocol.evidence_based_support.clinical_trials.map((trial, i) => (
                            <li key={i}>• {trial}</li>
                          ))}
                        </ul>
                      </Card>
                    )}
                    {generatedProtocol.evidence_based_support.pubmed_links && (
                      <Card className="p-4">
                        <h4 className="font-medium mb-2">PubMed References</h4>
                        <ul className="text-sm text-gray-600 space-y-1">
                          {generatedProtocol.evidence_based_support.pubmed_links.map((link, i) => (
                            <li key={i}>• <a href={link} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">{link}</a></li>
                          ))}
                        </ul>
                      </Card>
                    )}
                  </div>
                </div>
              )}

              {/* Outcome Statistics */}
              {generatedProtocol.outcome_statistics && (
                <div>
                  <h3 className="font-semibold mb-4 flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-green-600" />
                    Expected Outcomes & Statistics
                  </h3>
                  <div className="grid md:grid-cols-3 gap-4">
                    {Object.entries(generatedProtocol.outcome_statistics).map(([metric, value]) => (
                      <Card key={metric} className="p-4 text-center">
                        <div className="text-2xl font-bold text-green-600 mb-1">
                          {value === "Not available" ? "N/A" : value}
                        </div>
                        <div className="text-sm text-gray-600 capitalize">
                          {metric.replace(/_/g, ' ')}
                        </div>
                      </Card>
                    ))}
                  </div>
                </div>
              )}

              {/* Supporting Peptides */}
              {generatedProtocol.supporting_peptides && generatedProtocol.supporting_peptides.length > 0 && (
                <div>
                  <h3 className="font-semibold mb-4">Supporting Peptides</h3>
                  <div className="grid gap-2">
                    {generatedProtocol.supporting_peptides.map((peptide, index) => (
                      <div key={index} className="p-3 bg-gray-50 rounded-lg">
                        <div className="font-medium">{peptide.name}</div>
                        <div className="text-sm text-gray-600">{peptide.indication || peptide.rationale} • {peptide.dosage || peptide.dosing}</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Expected Timeline */}
              {generatedProtocol.expected_outcomes && (
                <div>
                  <h3 className="font-semibold mb-4">Expected Timeline</h3>
                  <div className="space-y-2">
                    {Object.entries(generatedProtocol.expected_outcomes).map(([timeframe, outcome]) => (
                      <div key={timeframe} className="flex gap-4">
                        <Badge variant="outline">{timeframe}</Badge>
                        <span className="text-sm text-gray-600">{Array.isArray(outcome) ? outcome.join(', ') : outcome}</span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              <div className="flex gap-4 pt-4 border-t">
                <Button 
                  onClick={() => window.print()}
                  variant="outline"
                  className="flex items-center gap-2"
                >
                  <Download className="h-4 w-4" />
                  Download PDF
                </Button>
                <Button variant="outline" onClick={() => setCurrentView('chat')}>
                  <MessageCircle className="h-4 w-4 mr-2" />
                  Chat with Dr. Peptide
                </Button>
                <Button variant="outline" onClick={() => setCurrentView('home')}>
                  <User className="h-4 w-4 mr-2" />
                  New Assessment
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      );
    };

  const FeedbackSystem = () => (
    <div className="max-w-6xl mx-auto p-6 space-y-8">
      {/* Feedback Header */}
      <div className="text-center space-y-4">
        <h2 className="text-3xl font-bold">Protocol Feedback & Collective Intelligence</h2>
        <p className="text-lg text-muted-foreground max-w-3xl mx-auto">
          Your experience helps evolve our platform. Share feedback, report issues, and contribute to the collective medical intelligence that makes protocols better for everyone.
        </p>
      </div>

      {/* Feedback Options */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Protocol Follow-up */}
        <div className="border rounded-lg p-6 space-y-4">
          <div className="flex items-center space-x-3">
            <MessageCircle className="h-8 w-8 text-blue-500" />
            <h3 className="text-xl font-semibold">Dr. Peptide Follow-up</h3>
          </div>
          <p className="text-muted-foreground">
            Continue your conversation with Dr. Peptide about your protocol progress, ask questions, and get personalized adjustments.
          </p>
          <Button 
            onClick={() => setShowFeedbackChat(true)}
            className="w-full"
          >
            Start Follow-up Chat
          </Button>
        </div>

        {/* Protocol Feedback */}
        <div className="border rounded-lg p-6 space-y-4">
          <div className="flex items-center space-x-3">
            <Star className="h-8 w-8 text-yellow-500" />
            <h3 className="text-xl font-semibold">Rate Your Protocol</h3>
          </div>
          <p className="text-muted-foreground">
            Share detailed feedback about your protocol effectiveness, side effects, and outcomes to help improve recommendations for others.
          </p>
          <Button 
            onClick={() => setShowProtocolFeedback(true)}
            variant="outline" 
            className="w-full"
          >
            Submit Protocol Feedback
          </Button>
        </div>

        {/* Error Reporting */}
        <div className="border rounded-lg p-6 space-y-4">
          <div className="flex items-center space-x-3">
            <AlertTriangle className="h-8 w-8 text-red-500" />
            <h3 className="text-xl font-semibold">Report Issue</h3>
          </div>
          <p className="text-muted-foreground">
            Found incorrect information or AI hallucination? Report it to help us maintain accuracy and improve the platform for everyone.
          </p>
          <Button 
            onClick={() => setShowErrorReport(true)}
            variant="outline" 
            className="w-full"
          >
            Report Error
          </Button>
        </div>
      </div>

      {/* Collective Intelligence Stats */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 rounded-lg p-8">
        <h3 className="text-2xl font-bold text-center mb-6">Collective Intelligence Network</h3>
        <div className="grid md:grid-cols-4 gap-6 text-center">
          <div className="space-y-2">
            <div className="text-3xl font-bold text-blue-600">2,847</div>
            <div className="text-sm text-muted-foreground">Protocol Feedbacks</div>
          </div>
          <div className="space-y-2">
            <div className="text-3xl font-bold text-green-600">94.2%</div>
            <div className="text-sm text-muted-foreground">Success Rate</div>
          </div>
          <div className="space-y-2">
            <div className="text-3xl font-bold text-purple-600">156</div>
            <div className="text-sm text-muted-foreground">Expert Practitioners</div>
          </div>
          <div className="space-y-2">
            <div className="text-3xl font-bold text-orange-600">89</div>
            <div className="text-sm text-muted-foreground">Corrections Applied</div>
          </div>
        </div>
        <div className="text-center mt-6">
          <p className="text-muted-foreground">
            Our AI learns from every interaction, making protocols smarter and safer through collective expertise.
          </p>
        </div>
      </div>

      {/* How It Works */}
      <div className="space-y-6">
        <h3 className="text-2xl font-bold text-center">How Collective Intelligence Works</h3>
        <div className="grid md:grid-cols-3 gap-6">
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto">
              <Users className="h-8 w-8 text-blue-600" />
            </div>
            <h4 className="text-lg font-semibold">Collective Input</h4>
            <p className="text-sm text-muted-foreground">
              Practitioners, patients, and AI agents contribute knowledge, feedback, and corrections to continuously improve protocols.
            </p>
          </div>
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto">
              <Brain className="h-8 w-8 text-green-600" />
            </div>
            <h4 className="text-lg font-semibold">AI Learning</h4>
            <p className="text-sm text-muted-foreground">
              Machine learning algorithms analyze patterns, outcomes, and feedback to optimize recommendations and catch errors.
            </p>
          </div>
          <div className="text-center space-y-4">
            <div className="w-16 h-16 bg-purple-100 rounded-full flex items-center justify-center mx-auto">
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
            <h4 className="text-lg font-semibold">Continuous Evolution</h4>
            <p className="text-sm text-muted-foreground">
              The platform evolves in real-time, providing increasingly accurate and personalized protocols based on collective wisdom.
            </p>
          </div>
        </div>
      </div>

      {/* Feedback Chat Modal */}
      {showFeedbackChat && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold">Dr. Peptide Follow-up Chat</h3>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => setShowFeedbackChat(false)}
              >
                ✕
              </Button>
            </div>
            
            <div className="space-y-4 mb-6">
              <div className="bg-blue-50 p-4 rounded-lg">
                <p className="text-sm text-blue-800">
                  👋 Hi! I'm here to follow up on your protocol experience. How are you feeling, and do you have any questions or concerns about your current protocol?
                </p>
              </div>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">How are you doing with your protocol?</label>
                <textarea 
                  ref={feedbackChatInputRef}
                  className="w-full p-3 border border-gray-300 rounded-md h-24"
                  placeholder="Tell me about your progress, any side effects, questions, or concerns..."
                />
              </div>
              <div className="flex space-x-3">
                <Button 
                  onClick={sendFeedbackChat}
                  disabled={loadingFeedbackChat}
                  className="flex-1"
                >
                  {loadingFeedbackChat ? 'Dr. Peptide is thinking...' : 'Send to Dr. Peptide'}
                </Button>
              </div>
            </div>

            {feedbackChatResponse && (
              <div className="mt-6 p-4 bg-green-50 rounded-lg">
                <h4 className="font-medium text-green-800 mb-2">Dr. Peptide Response:</h4>
                <div className="text-sm text-green-700 whitespace-pre-wrap">
                  {feedbackChatResponse}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Protocol Feedback Modal */}
      {showProtocolFeedback && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-3xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold">Protocol Feedback</h3>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => setShowProtocolFeedback(false)}
              >
                ✕
              </Button>
            </div>

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium mb-2">Overall Protocol Effectiveness</label>
                <div className="flex space-x-2">
                  {[1,2,3,4,5].map(rating => (
                    <Button
                      key={rating}
                      variant={protocolRating === rating ? "default" : "outline"}
                      size="sm"
                      onClick={() => setProtocolRating(rating)}
                    >
                      {rating} ⭐
                    </Button>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Specific Improvements Noticed</label>
                <div className="grid grid-cols-2 gap-2">
                  {['Energy', 'Sleep', 'Weight Loss', 'Mood', 'Cognitive Function', 'Physical Recovery'].map(improvement => (
                    <label key={improvement} className="flex items-center space-x-2">
                      <input 
                        type="checkbox" 
                        onChange={(e) => {
                          const current = improvementsNoticed.includes(improvement);
                          if (current) {
                            setImprovementsNoticed(improvementsNoticed.filter(i => i !== improvement));
                          } else {
                            setImprovementsNoticed([...improvementsNoticed, improvement]);
                          }
                        }}
                      />
                      <span className="text-sm">{improvement}</span>
                    </label>
                  ))}
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Side Effects Experienced (if any)</label>
                <textarea 
                  ref={sideEffectsRef}
                  className="w-full p-3 border border-gray-300 rounded-md h-20"
                  placeholder="Describe any side effects..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Additional Feedback & Suggestions</label>
                <textarea 
                  ref={additionalFeedbackRef}
                  className="w-full p-3 border border-gray-300 rounded-md h-24"
                  placeholder="Any other feedback, suggestions for improvement, or insights that might help other patients..."
                />
              </div>

              <Button 
                onClick={submitProtocolFeedback}
                disabled={loadingProtocolFeedback}
                className="w-full"
              >
                {loadingProtocolFeedback ? 'Submitting Feedback...' : 'Submit Feedback'}
              </Button>
            </div>

            {protocolFeedbackResponse && (
              <div className="mt-6 p-4 bg-green-50 rounded-lg">
                <h4 className="font-medium text-green-800 mb-2">Thank You!</h4>
                <div className="text-sm text-green-700 whitespace-pre-wrap">
                  {protocolFeedbackResponse}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Error Report Modal */}
      {showErrorReport && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-8 max-w-2xl w-full mx-4 max-h-[80vh] overflow-y-auto">
            <div className="flex justify-between items-center mb-6">
              <h3 className="text-xl font-bold">Report Error or Issue</h3>
              <Button 
                variant="ghost" 
                size="sm" 
                onClick={() => setShowErrorReport(false)}
              >
                ✕
              </Button>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-2">What type of issue are you reporting?</label>
                <select 
                  ref={errorTypeRef}
                  className="w-full p-3 border border-gray-300 rounded-md"
                >
                  <option value="incorrect_information">Incorrect Medical Information</option>
                  <option value="ai_hallucination">AI Hallucination/Made-up Content</option>
                  <option value="dosing_error">Incorrect Dosing Information</option>
                  <option value="safety_concern">Safety Concern</option>
                  <option value="other">Other Issue</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Describe the incorrect information</label>
                <textarea 
                  ref={incorrectInfoRef}
                  className="w-full p-3 border border-gray-300 rounded-md h-24"
                  placeholder="What specific information was incorrect?"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Provide the correct information</label>
                <textarea 
                  ref={correctInfoRef}
                  className="w-full p-3 border border-gray-300 rounded-md h-24"
                  placeholder="What is the correct information? Include sources if possible..."
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Severity Level</label>
                <select 
                  ref={severityRef}
                  className="w-full p-3 border border-gray-300 rounded-md"
                >
                  <option value="low">Low - Minor inaccuracy</option>
                  <option value="medium">Medium - Potentially misleading</option>
                  <option value="high">High - Potentially dangerous</option>
                </select>
              </div>

              <Button 
                onClick={submitErrorReport}
                disabled={loadingErrorReport}
                className="w-full"
              >
                {loadingErrorReport ? 'Submitting Report...' : 'Submit Error Report'}
              </Button>
            </div>

            {errorReportResponse && (
              <div className="mt-6 p-4 bg-blue-50 rounded-lg">
                <h4 className="font-medium text-blue-800 mb-2">Report Received</h4>
                <div className="text-sm text-blue-700 whitespace-pre-wrap">
                  {errorReportResponse}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );

  const ProgressDashboard = () => {
    const [localProgressData, setLocalProgressData] = React.useState(null);
    const [localLoadingProgress, setLocalLoadingProgress] = React.useState(false);
    
    // Load sample progress data for demonstration
    const loadProgressData = async () => {
      setLocalLoadingProgress(true);
      try {
        // For now, using sample data. In production, this would fetch from API
        const sampleProgressData = {
          patient_id: "demo_patient",
          protocol_id: "demo_protocol_001", 
          start_date: "2024-06-01T00:00:00",
          status: "active",
          chart_data: {
            time_series: {
              energy_levels: [
                { date: "2024-06-01", value: 4, unit: "1-10 scale", target: 7 },
                { date: "2024-06-15", value: 5, unit: "1-10 scale", target: 7 },
                { date: "2024-07-01", value: 6, unit: "1-10 scale", target: 7 },
                { date: "2024-07-15", value: 7, unit: "1-10 scale", target: 7 },
                { date: "2024-08-01", value: 8, unit: "1-10 scale", target: 7 },
                { date: "2024-08-09", value: 8.5, unit: "1-10 scale", target: 7 }
              ],
              sleep_quality: [
                { date: "2024-06-01", value: 3, unit: "1-10 scale", target: 7 },
                { date: "2024-06-15", value: 4, unit: "1-10 scale", target: 7 },
                { date: "2024-07-01", value: 5, unit: "1-10 scale", target: 7 },
                { date: "2024-07-15", value: 6, unit: "1-10 scale", target: 7 },
                { date: "2024-08-01", value: 7, unit: "1-10 scale", target: 7 },
                { date: "2024-08-09", value: 7.5, unit: "1-10 scale", target: 7 }
              ],
              weight: [
                { date: "2024-06-01", value: 185, unit: "lbs" },
                { date: "2024-06-15", value: 183, unit: "lbs" },
                { date: "2024-07-01", value: 180, unit: "lbs" },
                { date: "2024-07-15", value: 177, unit: "lbs" },
                { date: "2024-08-01", value: 173, unit: "lbs" },
                { date: "2024-08-09", value: 170, unit: "lbs" }
              ],
              hba1c: [
                { date: "2024-06-01", value: 6.1, unit: "%", target: 5.5, normal_min: 4.0, normal_max: 5.6 },
                { date: "2024-07-01", value: 5.8, unit: "%", target: 5.5, normal_min: 4.0, normal_max: 5.6 },
                { date: "2024-08-01", value: 5.4, unit: "%", target: 5.5, normal_min: 4.0, normal_max: 5.6 }
              ],
              crp: [
                { date: "2024-06-01", value: 3.8, unit: "mg/L", target: 1.0, normal_max: 3.0 },
                { date: "2024-07-01", value: 2.1, unit: "mg/L", target: 1.0, normal_max: 3.0 },
                { date: "2024-08-01", value: 1.2, unit: "mg/L", target: 1.0, normal_max: 3.0 }
              ]
            },
            progress_comparison: [
              { metric: "Energy Levels", current: 8.5, unit: "1-10", status: "normal", target: 7 },
              { metric: "Sleep Quality", current: 7.5, unit: "1-10", status: "normal", target: 7 },
              { metric: "Weight", current: 170, unit: "lbs", status: "normal", target: 170 },
              { metric: "HbA1c", current: 5.4, unit: "%", status: "normal", target: 5.5 },
              { metric: "C-Reactive Protein", current: 1.2, unit: "mg/L", status: "normal", target: 1.0 }
            ]
          },
          progress_scores: {
            overall_improvement: 78,
            symptom_improvement: 85,
            biomarker_improvement: 72,
            lifestyle_improvement: 76
          },
          achieved_milestones: [
            {
              name: "Energy Improvement",
              description: "Energy levels reached healthy range (7+)",
              achieved_date: "2024-07-15T00:00:00"
            },
            {
              name: "Sleep Quality Achievement",
              description: "Sleep quality reached optimal range (7+)",
              achieved_date: "2024-08-01T00:00:00"
            },
            {
              name: "Weight Loss Milestone",
              description: "Achieved 15+ lbs weight loss",
              achieved_date: "2024-08-09T00:00:00"
            }
          ],
          upcoming_milestones: [
            {
              name: "HbA1c Optimization",
              description: "Reach target HbA1c of 5.5%",
              current_progress: "5.4/5.5%",
              completion_percentage: 95
            }
          ],
          timeline_events: [
            {
              date: "2024-06-01T00:00:00",
              type: "start",
              title: "Protocol Started",
              description: "Began functional medicine protocol"
            },
            {
              date: "2024-07-15T00:00:00",
              type: "milestone",
              title: "Energy Improvement",
              description: "Energy levels reached healthy range (7+)"
            },
            {
              date: "2024-08-01T00:00:00",
              type: "milestone",
              title: "Sleep Quality Achievement", 
              description: "Sleep quality reached optimal range (7+)"
            },
            {
              date: "2024-08-09T00:00:00",
              type: "milestone",
              title: "Weight Loss Milestone",
              description: "Achieved 15+ lbs weight loss"
            }
          ],
          total_days: 70,
          notes_count: 12,
          metrics_count: 23
        };
        
        setLocalProgressData(sampleProgressData);
      } catch (error) {
        console.error('Error loading progress data:', error);
      } finally {
        setLocalLoadingProgress(false);
      }
    };

    React.useEffect(() => {
      if (currentView === 'dashboard') {
        loadProgressData();
      }
    }, [currentView]);

    if (localLoadingProgress) {
      return (
        <div className="max-w-6xl mx-auto p-6">
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <Activity className="h-8 w-8 animate-spin mx-auto mb-4" />
              <p>Loading progress dashboard...</p>
            </div>
          </div>
        </div>
      );
    }

    if (!localProgressData) {
      return (
        <div className="max-w-6xl mx-auto p-6">
          <div className="text-center space-y-4">
            <Activity className="h-16 w-16 mx-auto text-gray-400" />
            <h2 className="text-2xl font-bold">Progress Dashboard</h2>
            <p className="text-muted-foreground">No progress data available. Start a protocol to begin tracking.</p>
          </div>
        </div>
      );
    }

    // Chart color scheme
    const COLORS = ['#2563eb', '#16a34a', '#dc2626', '#ca8a04', '#9333ea', '#0891b2'];

    return (
      <div className="max-w-6xl mx-auto p-6 space-y-8">
        {/* Dashboard Header */}
        <div className="space-y-4">
          <h1 className="text-3xl font-bold flex items-center">
            <Activity className="h-8 w-8 mr-3 text-blue-600" />
            Progress Dashboard
          </h1>
          <p className="text-lg text-muted-foreground">
            Comprehensive patient progress tracking with advanced analytics and milestone monitoring
          </p>
        </div>

        {/* Key Performance Indicators */}
        <div className="grid md:grid-cols-4 gap-6">
          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Overall Progress</p>
                <p className="text-2xl font-bold text-green-600">{localProgressData.progress_scores.overall_improvement.toFixed(0)}%</p>
              </div>
              <TrendingUp className="h-8 w-8 text-green-600" />
            </div>
            <div className="mt-4">
              <Progress value={localProgressData.progress_scores.overall_improvement} className="h-2" />
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Days Active</p>
                <p className="text-2xl font-bold">{localProgressData.total_days}</p>
              </div>
              <Clock className="h-8 w-8 text-blue-600" />
            </div>
            <div className="mt-4 text-sm text-muted-foreground">
              Started {format(parseISO(localProgressData.start_date), 'MMM d, yyyy')}
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Milestones</p>
                <p className="text-2xl font-bold text-purple-600">{localProgressData.achieved_milestones.length}</p>
              </div>
              <Award className="h-8 w-8 text-purple-600" />
            </div>
            <div className="mt-4 text-sm text-muted-foreground">
              {localProgressData.upcoming_milestones.length} upcoming
            </div>
          </Card>

          <Card className="p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-muted-foreground">Data Points</p>
                <p className="text-2xl font-bold">{localProgressData.metrics_count}</p>
              </div>
              <Activity className="h-8 w-8 text-orange-600" />
            </div>
            <div className="mt-4 text-sm text-muted-foreground">
              {localProgressData.notes_count} notes recorded
            </div>
          </Card>
        </div>

        {/* Progress Charts Section */}
        <div className="grid md:grid-cols-2 gap-8">
          {/* Energy & Sleep Trends */}
          <Card className="p-6">
            <h3 className="text-xl font-semibold mb-4">Symptom Improvement Trends</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={
                localProgressData.chart_data.time_series.energy_levels.map((energy, index) => ({
                  date: format(parseISO(energy.date), 'MMM d'),
                  energy: energy.value,
                  sleep: localProgressData.chart_data.time_series.sleep_quality[index]?.value || 0,
                  energyTarget: energy.target,
                  sleepTarget: localProgressData.chart_data.time_series.sleep_quality[index]?.target || 7
                }))
              }>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis domain={[0, 10]} />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="energy" stroke="#2563eb" strokeWidth={3} name="Energy Levels" />
                <Line type="monotone" dataKey="sleep" stroke="#16a34a" strokeWidth={3} name="Sleep Quality" />
                <Line type="monotone" dataKey="energyTarget" stroke="#93c5fd" strokeDasharray="5 5" name="Energy Target" />
                <Line type="monotone" dataKey="sleepTarget" stroke="#86efac" strokeDasharray="5 5" name="Sleep Target" />
              </LineChart>
            </ResponsiveContainer>
          </Card>

          {/* Weight Loss Progress */}
          <Card className="p-6">
            <h3 className="text-xl font-semibold mb-4">Weight Loss Progress</h3>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={
                localProgressData.chart_data.time_series.weight.map(point => ({
                  date: format(parseISO(point.date), 'MMM d'),
                  weight: point.value,
                  loss: 185 - point.value // Starting weight was 185
                }))
              }>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="weight" stroke="#dc2626" fill="#fca5a5" strokeWidth={2} name="Current Weight (lbs)" />
              </AreaChart>
            </ResponsiveContainer>
            <div className="mt-4 text-center">
              <p className="text-2xl font-bold text-green-600">-15 lbs</p>
              <p className="text-sm text-muted-foreground">Total Weight Loss</p>
            </div>
          </Card>
        </div>

        {/* Biomarker Progress */}
        <Card className="p-6">
          <h3 className="text-xl font-semibold mb-4">Biomarker Improvements</h3>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <h4 className="font-semibold mb-3">HbA1c Trend</h4>
              <ResponsiveContainer width="100%" height={200}>
                <LineChart data={
                  localProgressData.chart_data.time_series.hba1c.map(point => ({
                    date: format(parseISO(point.date), 'MMM'),
                    value: point.value,
                    target: point.target,
                    normalMax: point.normal_max
                  }))
                }>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis domain={[4, 7]} />
                  <Tooltip />
                  <Line type="monotone" dataKey="value" stroke="#dc2626" strokeWidth={3} name="HbA1c" />
                  <Line type="monotone" dataKey="target" stroke="#16a34a" strokeDasharray="5 5" name="Target" />
                  <Line type="monotone" dataKey="normalMax" stroke="#f59e0b" strokeDasharray="3 3" name="Normal Max" />
                </LineChart>
              </ResponsiveContainer>
            </div>
            
            <div>
              <h4 className="font-semibold mb-3">Inflammation (CRP)</h4>
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={
                  localProgressData.chart_data.time_series.crp.map(point => ({
                    date: format(parseISO(point.date), 'MMM'),
                    value: point.value,
                    target: point.target,
                    normalMax: point.normal_max
                  }))
                }>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="value" fill="#2563eb" name="CRP (mg/L)" />
                  <Line type="monotone" dataKey="normalMax" stroke="#dc2626" strokeDasharray="3 3" name="Normal Max" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </Card>

        {/* Progress Scores Radar Chart */}
        <Card className="p-6">
          <h3 className="text-xl font-semibold mb-4">Multi-Dimensional Progress Analysis</h3>
          <div className="grid md:grid-cols-2 gap-8">
            <div>
              <ResponsiveContainer width="100%" height={300}>
                <RadarChart data={[
                  {
                    category: 'Symptoms',
                    score: localProgressData.progress_scores.symptom_improvement,
                    fullMark: 100
                  },
                  {
                    category: 'Biomarkers', 
                    score: localProgressData.progress_scores.biomarker_improvement,
                    fullMark: 100
                  },
                  {
                    category: 'Lifestyle',
                    score: localProgressData.progress_scores.lifestyle_improvement,
                    fullMark: 100
                  },
                  {
                    category: 'Overall',
                    score: localProgressData.progress_scores.overall_improvement,
                    fullMark: 100
                  }
                ]}>
                  <PolarGrid />
                  <PolarAngleAxis dataKey="category" />
                  <PolarRadiusAxis domain={[0, 100]} />
                  <Radar name="Progress Score" dataKey="score" stroke="#2563eb" fill="#2563eb" fillOpacity={0.3} strokeWidth={2} />
                </RadarChart>
              </ResponsiveContainer>
            </div>

            <div className="space-y-4">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium">Symptom Improvement</span>
                  <span className="font-bold text-green-600">{localProgressData.progress_scores.symptom_improvement.toFixed(0)}%</span>
                </div>
                <Progress value={localProgressData.progress_scores.symptom_improvement} className="h-3" />
              </div>

              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium">Biomarker Improvement</span>
                  <span className="font-bold text-blue-600">{localProgressData.progress_scores.biomarker_improvement.toFixed(0)}%</span>
                </div>
                <Progress value={localProgressData.progress_scores.biomarker_improvement} className="h-3" />
              </div>

              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="font-medium">Lifestyle Improvement</span>
                  <span className="font-bold text-purple-600">{localProgressData.progress_scores.lifestyle_improvement.toFixed(0)}%</span>
                </div>
                <Progress value={localProgressData.progress_scores.lifestyle_improvement} className="h-3" />
              </div>

              <div className="pt-4 border-t">
                <div className="flex justify-between items-center mb-2">
                  <span className="font-semibold text-lg">Overall Progress</span>
                  <span className="font-bold text-2xl text-green-600">{localProgressData.progress_scores.overall_improvement.toFixed(0)}%</span>
                </div>
                <Progress value={localProgressData.progress_scores.overall_improvement} className="h-4" />
              </div>
            </div>
          </div>
        </Card>

        {/* Milestones & Timeline */}
        <div className="grid md:grid-cols-2 gap-8">
          <Card className="p-6">
            <h3 className="text-xl font-semibold mb-4">Achieved Milestones</h3>
            <div className="space-y-4">
              {localProgressData.achieved_milestones.map((milestone, index) => (
                <div key={index} className="flex items-center space-x-3 p-3 bg-green-50 rounded-lg border border-green-200">
                  <Award className="h-6 w-6 text-green-600" />
                  <div>
                    <p className="font-semibold text-green-800">{milestone.name}</p>
                    <p className="text-sm text-green-600">{milestone.description}</p>
                    <p className="text-xs text-green-500">
                      Achieved {format(parseISO(milestone.achieved_date), 'MMM d, yyyy')}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {localProgressData.upcoming_milestones.length > 0 && (
              <div className="mt-6">
                <h4 className="font-semibold mb-3">Upcoming Milestones</h4>
                {localProgressData.upcoming_milestones.map((milestone, index) => (
                  <div key={index} className="p-3 bg-blue-50 rounded-lg border border-blue-200">
                    <p className="font-semibold text-blue-800">{milestone.name}</p>
                    <p className="text-sm text-blue-600">{milestone.description}</p>
                    <div className="mt-2">
                      <Progress value={milestone.completion_percentage} className="h-2" />
                      <p className="text-xs text-blue-500 mt-1">
                        {milestone.completion_percentage.toFixed(0)}% complete
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>

          <Card className="p-6">
            <h3 className="text-xl font-semibold mb-4">Progress Timeline</h3>
            <div className="space-y-4 max-h-96 overflow-y-auto">
              {localProgressData.timeline_events.map((event, index) => (
                <div key={index} className="flex items-start space-x-3">
                  <div className={`w-3 h-3 rounded-full mt-2 ${
                    event.type === 'start' ? 'bg-blue-500' :
                    event.type === 'milestone' ? 'bg-green-500' : 'bg-purple-500'
                  }`}></div>
                  <div>
                    <p className="font-semibold">{event.title}</p>
                    <p className="text-sm text-muted-foreground">{event.description}</p>
                    <p className="text-xs text-gray-400">
                      {format(parseISO(event.date), 'MMM d, yyyy')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </Card>
        </div>

        {/* Current Status Summary */}
        <Card className="p-6 bg-gradient-to-r from-blue-50 to-green-50">
          <h3 className="text-xl font-semibold mb-4">Current Status Summary</h3>
          <div className="grid md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-semibold mb-2">Key Improvements</h4>
              <ul className="text-sm space-y-1">
                <li>• Energy levels increased by 112% (4 → 8.5)</li>
                <li>• Sleep quality improved by 150% (3 → 7.5)</li>
                <li>• 15 lbs weight loss achieved</li>
                <li>• HbA1c normalized (6.1% → 5.4%)</li>
                <li>• Inflammation reduced 68% (3.8 → 1.2 mg/L)</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2">Next Focus Areas</h4>
              <ul className="text-sm space-y-1">
                <li>• Continue weight optimization</li>
                <li>• Maintain current energy levels</li>
                <li>• Further CRP reduction</li>
                <li>• HbA1c stabilization</li>
                <li>• Long-term maintenance planning</li>
              </ul>
            </div>
            
            <div>
              <h4 className="font-semibold mb-2">Protocol Effectiveness</h4>
              <div className="space-y-2">
                <div className="flex justify-between text-sm">
                  <span>Overall Success Rate:</span>
                  <span className="font-bold text-green-600">78%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Treatment Adherence:</span>
                  <span className="font-bold text-blue-600">94%</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Side Effects:</span>
                  <span className="font-bold text-green-600">Minimal</span>
                </div>
                <div className="flex justify-between text-sm">
                  <span>Patient Satisfaction:</span>
                  <span className="font-bold text-green-600">Excellent</span>
                </div>
              </div>
            </div>
          </div>
        </Card>
      </div>
    );
  };

  const Navigation = () => {
    const navigationItems = [
      { id: 'home', label: 'Home', icon: null },
      { id: 'assessment', label: 'Assessment', icon: null },
      { id: 'chat', label: 'Dr. Peptide', icon: MessageCircle },
      { id: 'progress', label: 'Progress Tracking', icon: Activity },
      { id: 'protocols', label: 'Protocols', icon: BookOpen },
      { id: 'peptides', label: 'Peptides', icon: FlaskConical },
      { id: 'network', label: 'Network', icon: Network },
      { id: 'feedback', label: 'Feedback', icon: MessageCircle },
      { id: 'dashboard', label: 'Dashboard', icon: Activity }
    ];

    const handleNavClick = (viewId) => {
      setCurrentView(viewId);
      setIsMobileMenuOpen(false); // Close mobile menu after navigation
    };

    return (
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center gap-3 cursor-pointer" onClick={() => handleNavClick('home')}>
              <Brain className="h-8 w-8 text-blue-600" />
              <span className="text-xl md:text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                PeptideProtocols.ai
              </span>
            </div>
            
            {/* Desktop Navigation */}
            <div className="hidden md:flex gap-1">
              {navigationItems.map((item) => (
                <Button 
                  key={item.id}
                  variant={currentView === item.id ? 'default' : 'ghost'}
                  onClick={() => handleNavClick(item.id)}
                  size="sm"
                >
                  {item.icon && <item.icon className="h-4 w-4 mr-1" />}
                  {item.label}
                </Button>
              ))}
            </div>

            {/* Mobile Hamburger Menu Button */}
            <div className="md:hidden">
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
                className="p-2"
                aria-label={`${isMobileMenuOpen ? 'Close' : 'Open'} navigation menu`}
                aria-expanded={isMobileMenuOpen}
                aria-controls="mobile-menu"
              >
                {isMobileMenuOpen ? (
                  <X className="h-6 w-6" aria-hidden="true" />
                ) : (
                  <Menu className="h-6 w-6" aria-hidden="true" />
                )}
              </Button>
            </div>
          </div>

          {/* Mobile Menu Overlay */}
          {isMobileMenuOpen && (
            <div 
              id="mobile-menu"
              className="md:hidden absolute left-0 right-0 top-16 bg-white border-b border-gray-200 shadow-lg z-40"
              role="navigation"
              aria-label="Mobile navigation menu"
            >
              <div className="px-4 py-2 space-y-1">
                {navigationItems.map((item) => (
                  <Button
                    key={item.id}
                    variant={currentView === item.id ? 'default' : 'ghost'}
                    onClick={() => handleNavClick(item.id)}
                    className="w-full justify-start text-left"
                    aria-label={`Navigate to ${item.label} page`}
                  >
                    {item.icon && <item.icon className="h-4 w-4 mr-2" aria-hidden="true" />}
                    {item.label}
                  </Button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Mobile Menu Backdrop */}
        {isMobileMenuOpen && (
          <div 
            className="md:hidden fixed inset-0 bg-black bg-opacity-25 z-30"
            onClick={() => setIsMobileMenuOpen(false)}
          />
        )}
      </nav>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <Navigation />
      
      {currentView === 'home' && <HomePage />}
      {currentView === 'assessment' && <AssessmentWizard />}
      {currentView === 'chat' && <DrPeptideChat />}
      {currentView === 'progress' && <ProgressTracking patientId={assessment.patient_name} />}
      {currentView === 'protocols' && <ProtocolLibrary />}
      {currentView === 'peptides' && <PeptidesView />}
      {currentView === 'network' && <CollectiveIntelligenceNetwork />}
      {currentView === 'feedback' && <FeedbackSystem />}
      {currentView === 'dashboard' && <ProgressDashboard />}
      {currentView === 'protocol' && <ProtocolView />}
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<PeptideProtocolsApp />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;