import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { Label } from "./ui/label";
import { Badge } from "./ui/badge";
import { Progress } from "./ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "./ui/tabs";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { TrendingUp, Award, Activity, Target, Plus, Calendar } from "lucide-react";

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;

const ProgressTracking = ({ patientId }) => {
  const [progressData, setProgressData] = useState(null);
  const [analytics, setAnalytics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [metricInput, setMetricInput] = useState({
    energy_levels: '',
    sleep_quality: '',
    weight: '',
    joint_pain: '',
    cognitive_function: '',
    notes: ''
  });

  useEffect(() => {
    if (patientId) {
      fetchProgressData();
      fetchAnalytics();
    }
  }, [patientId]);

  const fetchProgressData = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${BACKEND_URL}/api/progress/${patientId}`);
      const data = await response.json();
      
      if (data.success) {
        setProgressData(data.progress_data);
      }
    } catch (error) {
      console.error('Error fetching progress data:', error);
    } finally {
      setLoading(false);
    }
  };

  const fetchAnalytics = async () => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/progress/${patientId}/analytics?time_period=30d`);
      const data = await response.json();
      
      if (data.success) {
        setAnalytics(data.analytics);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  const submitProgressUpdate = async () => {
    try {
      setLoading(true);
      
      // Filter out empty values
      const metricUpdates = {};
      Object.keys(metricInput).forEach(key => {
        if (metricInput[key] && metricInput[key] !== '' && key !== 'notes') {
          metricUpdates[key] = parseFloat(metricInput[key]) || metricInput[key];
        }
      });

      const response = await fetch(`${BACKEND_URL}/api/progress/track`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          patient_id: patientId,
          metric_updates: metricUpdates,
          notes: metricInput.notes || ''
        })
      });

      const data = await response.json();
      
      if (data.success) {
        // Clear form
        setMetricInput({
          energy_levels: '',
          sleep_quality: '',
          weight: '',
          joint_pain: '',
          cognitive_function: '',
          notes: ''
        });
        
        // Refresh data
        await fetchProgressData();
        await fetchAnalytics();
      }
    } catch (error) {
      console.error('Error submitting progress:', error);
    } finally {
      setLoading(false);
    }
  };

  const trackMilestone = async (milestoneData) => {
    try {
      const response = await fetch(`${BACKEND_URL}/api/progress/${patientId}/milestone`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          milestone_data: milestoneData
        })
      });

      const data = await response.json();
      
      if (data.success) {
        await fetchProgressData();
      }
    } catch (error) {
      console.error('Error tracking milestone:', error);
    }
  };

  if (!patientId) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Progress Tracking</CardTitle>
          <CardDescription>
            Complete an assessment and generate a protocol to start tracking progress
          </CardDescription>
        </CardHeader>
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Progress Tracking Dashboard</h2>
        <Badge variant="secondary">
          <Activity className="w-4 h-4 mr-2" />
          Patient ID: {patientId}
        </Badge>
      </div>

      <Tabs defaultValue="overview" className="space-y-4">
        <TabsList>
          <TabsTrigger value="overview">Overview</TabsTrigger>
          <TabsTrigger value="metrics">Update Metrics</TabsTrigger>
          <TabsTrigger value="analytics">Analytics</TabsTrigger>
          <TabsTrigger value="milestones">Milestones</TabsTrigger>
        </TabsList>

        <TabsContent value="overview">
          {progressData ? (
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {/* Progress Scores */}
              {progressData.progress_scores && (
                <>
                  <Card>
                    <CardHeader>
                      <CardTitle className="flex items-center">
                        <TrendingUp className="w-5 h-5 mr-2 text-green-600" />
                        Overall Progress
                      </CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-green-600">
                        {Math.round(progressData.progress_scores.overall_improvement)}%
                      </div>
                      <Progress value={progressData.progress_scores.overall_improvement} className="mt-2" />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Symptom Improvement</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-blue-600">
                        {Math.round(progressData.progress_scores.symptom_improvement)}%
                      </div>
                      <Progress value={progressData.progress_scores.symptom_improvement} className="mt-2" />
                    </CardContent>
                  </Card>

                  <Card>
                    <CardHeader>
                      <CardTitle>Lifestyle Changes</CardTitle>
                    </CardHeader>
                    <CardContent>
                      <div className="text-2xl font-bold text-purple-600">
                        {Math.round(progressData.progress_scores.lifestyle_improvement)}%
                      </div>
                      <Progress value={progressData.progress_scores.lifestyle_improvement} className="mt-2" />
                    </CardContent>
                  </Card>
                </>
              )}

              {/* Latest Metrics */}
              {progressData.latest_metrics && Object.keys(progressData.latest_metrics).length > 0 && (
                <Card className="md:col-span-2">
                  <CardHeader>
                    <CardTitle>Latest Metrics</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="grid md:grid-cols-2 gap-4">
                      {Object.entries(progressData.latest_metrics).map(([metric, value]) => (
                        <div key={metric} className="flex justify-between items-center p-2 bg-gray-50 rounded">
                          <span className="font-medium capitalize">{metric.replace(/_/g, ' ')}</span>
                          <span className="text-lg font-bold">{value}</span>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          ) : (
            <Card>
              <CardHeader>
                <CardTitle>No Progress Data</CardTitle>
                <CardDescription>
                  Start tracking your progress by updating metrics in the "Update Metrics" tab
                </CardDescription>
              </CardHeader>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="metrics">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <Plus className="w-5 h-5 mr-2" />
                Update Progress Metrics
              </CardTitle>
              <CardDescription>
                Enter your current metrics to track progress over time
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label htmlFor="energy">Energy Levels (1-10)</Label>
                  <Input
                    id="energy"
                    type="number"
                    min="1"
                    max="10"
                    placeholder="Rate 1-10"
                    value={metricInput.energy_levels}
                    onChange={(e) => setMetricInput(prev => ({...prev, energy_levels: e.target.value}))}
                  />
                </div>

                <div>
                  <Label htmlFor="sleep">Sleep Quality (1-10)</Label>
                  <Input
                    id="sleep"
                    type="number"
                    min="1"
                    max="10"
                    placeholder="Rate 1-10"
                    value={metricInput.sleep_quality}
                    onChange={(e) => setMetricInput(prev => ({...prev, sleep_quality: e.target.value}))}
                  />
                </div>

                <div>
                  <Label htmlFor="weight">Weight (lbs)</Label>
                  <Input
                    id="weight"
                    type="number"
                    placeholder="Current weight"
                    value={metricInput.weight}
                    onChange={(e) => setMetricInput(prev => ({...prev, weight: e.target.value}))}
                  />
                </div>

                <div>
                  <Label htmlFor="joint_pain">Joint Pain (1-10, 1=no pain)</Label>
                  <Input
                    id="joint_pain"
                    type="number"
                    min="1"
                    max="10"
                    placeholder="Rate 1-10"
                    value={metricInput.joint_pain}
                    onChange={(e) => setMetricInput(prev => ({...prev, joint_pain: e.target.value}))}
                  />
                </div>

                <div className="md:col-span-2">
                  <Label htmlFor="cognitive">Cognitive Function (1-10)</Label>
                  <Input
                    id="cognitive"
                    type="number"
                    min="1"
                    max="10"
                    placeholder="Rate 1-10"
                    value={metricInput.cognitive_function}
                    onChange={(e) => setMetricInput(prev => ({...prev, cognitive_function: e.target.value}))}
                  />
                </div>

                <div className="md:col-span-2">
                  <Label htmlFor="notes">Notes (optional)</Label>
                  <Input
                    id="notes"
                    placeholder="Any additional notes about your progress..."
                    value={metricInput.notes}
                    onChange={(e) => setMetricInput(prev => ({...prev, notes: e.target.value}))}
                  />
                </div>
              </div>

              <Button 
                onClick={submitProgressUpdate}
                disabled={loading}
                className="w-full"
              >
                {loading ? 'Submitting...' : 'Update Progress'}
              </Button>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="analytics">
          {analytics ? (
            <div className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>30-Day Analytics</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="font-medium mb-2">Progress Summary</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span>Overall Improvement:</span>
                          <span className="font-bold">{Math.round(analytics.progress_summary?.overall_improvement || 0)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Symptom Improvement:</span>
                          <span className="font-bold">{Math.round(analytics.progress_summary?.symptom_improvement || 0)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Biomarker Improvement:</span>
                          <span className="font-bold">{Math.round(analytics.progress_summary?.biomarker_improvement || 0)}%</span>
                        </div>
                      </div>
                    </div>

                    <div>
                      <h4 className="font-medium mb-2">Data Quality</h4>
                      <div className="space-y-2">
                        <div className="flex justify-between">
                          <span>Total Entries:</span>
                          <span className="font-bold">{analytics.data_quality?.total_entries || 0}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Unique Metrics:</span>
                          <span className="font-bold">{analytics.data_quality?.unique_metrics || 0}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Consistency Score:</span>
                          <span className="font-bold">{Math.round(analytics.data_quality?.data_consistency || 0)}%</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </CardContent>
              </Card>

              {analytics.metric_trends && Object.keys(analytics.metric_trends).length > 0 && (
                <Card>
                  <CardHeader>
                    <CardTitle>Metric Trends</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-3">
                      {Object.entries(analytics.metric_trends).map(([metric, trend]) => (
                        <div key={metric} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                          <div>
                            <div className="font-medium capitalize">{metric.replace(/_/g, ' ')}</div>
                            <div className="text-sm text-gray-600">
                              {trend.data_points} data points
                            </div>
                          </div>
                          <div className="text-right">
                            <Badge variant={
                              trend.trend === 'improving' ? 'default' : 
                              trend.trend === 'stable' ? 'secondary' : 'destructive'
                            }>
                              {trend.trend}
                            </Badge>
                            <div className="text-sm font-medium">
                              {trend.change > 0 ? '+' : ''}{trend.change}
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              )}
            </div>
          ) : (
            <Card>
              <CardHeader>
                <CardTitle>No Analytics Available</CardTitle>
                <CardDescription>
                  Submit some progress metrics to generate analytics
                </CardDescription>
              </CardHeader>
            </Card>
          )}
        </TabsContent>

        <TabsContent value="milestones">
          <div className="space-y-4">
            {progressData?.achieved_milestones && progressData.achieved_milestones.length > 0 ? (
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center">
                    <Award className="w-5 h-5 mr-2 text-yellow-600" />
                    Achieved Milestones
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {progressData.achieved_milestones.map((milestone, index) => (
                      <div key={index} className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded">
                        <div>
                          <div className="font-medium text-green-800">{milestone.name}</div>
                          <div className="text-sm text-green-600">{milestone.description}</div>
                        </div>
                        <Badge variant="default" className="bg-green-600">
                          <Award className="w-3 h-3 mr-1" />
                          Achieved
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            ) : (
              <Card>
                <CardHeader>
                  <CardTitle>Milestones</CardTitle>
                  <CardDescription>
                    Complete your progress tracking to unlock milestone achievements
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-8">
                    <Target className="w-12 h-12 mx-auto text-gray-400 mb-4" />
                    <p className="text-gray-600">Start tracking metrics to see milestone progress</p>
                  </div>
                </CardContent>
              </Card>
            )}

            {progressData?.upcoming_milestones && progressData.upcoming_milestones.length > 0 && (
              <Card>
                <CardHeader>
                  <CardTitle>Upcoming Milestones</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    {progressData.upcoming_milestones.map((milestone, index) => (
                      <div key={index} className="p-3 border border-blue-200 bg-blue-50 rounded">
                        <div className="flex justify-between items-center mb-2">
                          <div className="font-medium text-blue-800">{milestone.name}</div>
                          <span className="text-sm font-medium text-blue-600">
                            {Math.round(milestone.completion_percentage)}%
                          </span>
                        </div>
                        <div className="text-sm text-blue-600 mb-2">{milestone.description}</div>
                        <Progress value={milestone.completion_percentage} className="h-2" />
                        <div className="text-xs text-blue-500 mt-1">
                          Current: {milestone.current_progress}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            )}
          </div>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default ProgressTracking;