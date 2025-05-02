import React, { useState, useEffect } from 'react';

function GasGaugeDashboard() {
  // Current session data - this would be dynamically updated in a real implementation
  const [sessionData, setSessionData] = useState({
    currentUsage: 30.5,
    warningThreshold: 60,
    hardStopThreshold: 90,
    sessionStartTime: new Date().toLocaleString(),
    sessionDuration: "15 minutes",
    status: "NORMAL",
    operations: [
      { type: "Context Loading", details: "80KB repository", usage: 10.0, cumulative: 10.0 },
      { type: "Discussion Exchange", details: "Initial greeting, ~100 words", usage: 5.5, cumulative: 15.5 },
      { type: "Search Operation", details: "Searched for previous session info", usage: 4.0, cumulative: 19.5 },
      { type: "Discussion Exchange", details: "Follow-up discussion, ~150 words", usage: 6.0, cumulative: 25.5 },
      { type: "Artifact Update", details: "Dashboard modification, medium complexity", usage: 5.0, cumulative: 30.5 }
    ],
    recommendations: [
      "Sufficient capacity for planned operations",
      "Continue with current work plan"
    ]
  });

  // Function to determine gauge color based on usage
  const getGaugeColor = (usage) => {
    if (usage >= sessionData.hardStopThreshold) return "bg-red-600";
    if (usage >= sessionData.warningThreshold) return "bg-yellow-500";
    if (usage >= sessionData.warningThreshold * 0.8) return "bg-yellow-300";
    return "bg-green-500";
  };

  // Function to determine status text color
  const getStatusColor = (status) => {
    switch (status) {
      case "CRITICAL": return "text-red-600 font-bold";
      case "WARNING": return "text-yellow-500 font-bold";
      case "CAUTION": return "text-yellow-400 font-bold";
      default: return "text-green-600 font-bold";
    }
  };

  // Add new operation to the session data
  const addOperation = (type, details, usage) => {
    const newUsage = sessionData.currentUsage + usage;
    const cumulative = newUsage;
    let status = "NORMAL";
    
    if (newUsage >= sessionData.hardStopThreshold) {
      status = "CRITICAL";
    } else if (newUsage >= sessionData.warningThreshold) {
      status = "WARNING";
    } else if (newUsage >= sessionData.warningThreshold * 0.8) {
      status = "CAUTION";
    }
    
    let recommendations = [];
    if (status === "CRITICAL") {
      recommendations = [
        "Emergency continuity generation required",
        "Hop immediately to avoid data loss"
      ];
    } else if (status === "WARNING") {
      recommendations = [
        "Prepare to wrap up current work",
        "Generate continuity documentation"
      ];
    } else if (status === "CAUTION") {
      recommendations = [
        "Approaching warning threshold",
        "Complete current high-priority tasks"
      ];
    } else {
      recommendations = [
        "Sufficient capacity for planned operations",
        "Continue with current work plan"
      ];
    }
    
    const newOperation = {
      type,
      details,
      usage,
      cumulative
    };
    
    setSessionData({
      ...sessionData,
      currentUsage: newUsage,
      status,
      recommendations,
      operations: [...sessionData.operations, newOperation],
      sessionDuration: `${Math.round((new Date() - new Date(sessionData.sessionStartTime)) / 60000)} minutes`
    });
  };

  // Operation cost reference
  const operationCosts = {
    contextLoading: { base: 2.0, perKb: 0.05 },
    codeGeneration: {
      base: { low: 3.0, medium: 6.0, high: 12.0 },
      sizeFactor: { small: 1.0, medium: 2.5, large: 5.0 }
    },
    discussionExchange: { base: 1.0, perWord: 0.01 },
    searchOperation: { base: 4.0, perResult: 0.5 },
    artifactCreation: {
      base: { low: 5.0, medium: 10.0, high: 17.5 },
      sizeFactor: { small: 1.0, medium: 2.0, large: 4.0 }
    }
  };

  // Simulate a user event handler
  const handleAddOperation = () => {
    addOperation("Code Generation", "Medium complexity, medium size", 15.0);
  };

  const handleAddDiscussion = () => {
    addOperation("Discussion Exchange", "~200 words", 6.0);
  };

  const handleAddArtifact = () => {
    addOperation("Artifact Creation", "Medium complexity, medium size", 20.0);
  };
  
  const handleAddSearch = () => {
    addOperation("Search Operation", "Web search with 5 results", 6.5);
  };

  return (
    <div className="bg-gray-100 p-6 rounded-lg shadow-lg w-full">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-800">TeamBadass Gas Gauge</h1>
        <div className="text-sm text-gray-600">
          Session started: {sessionData.sessionStartTime} · Duration: {sessionData.sessionDuration}
        </div>
      </div>

      {/* Main Gas Gauge */}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-1">
          <span className="text-lg font-semibold">Current Usage: {sessionData.currentUsage.toFixed(1)}%</span>
          <span className={getStatusColor(sessionData.status)}>
            {sessionData.status}
          </span>
        </div>
        <div className="h-8 w-full bg-gray-300 rounded-full relative overflow-hidden">
          {/* Filled portion */}
          <div 
            className={`h-full rounded-l-full ${getGaugeColor(sessionData.currentUsage)}`}
            style={{ width: `${sessionData.currentUsage}%` }}
          ></div>
          
          {/* Warning threshold marker */}
          <div 
            className="absolute top-0 bottom-0 w-1 bg-yellow-500"
            style={{ left: `${sessionData.warningThreshold}%` }}
          >
            <div className="absolute -top-6 -left-2 text-xs font-semibold">W</div>
          </div>
          
          {/* Hard stop threshold marker */}
          <div 
            className="absolute top-0 bottom-0 w-1 bg-red-600"
            style={{ left: `${sessionData.hardStopThreshold}%` }}
          >
            <div className="absolute -top-6 -left-2 text-xs font-semibold">H</div>
          </div>
        </div>
        <div className="flex justify-between text-xs mt-1">
          <span>0%</span>
          <span>W: {sessionData.warningThreshold}% (Warning)</span>
          <span>H: {sessionData.hardStopThreshold}% (Hard Stop)</span>
          <span>100%</span>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        <div className="bg-white p-4 rounded shadow">
          <div className="text-sm text-gray-500">Used Capacity</div>
          <div className="text-2xl font-bold">{sessionData.currentUsage.toFixed(1)}%</div>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <div className="text-sm text-gray-500">Remaining</div>
          <div className="text-2xl font-bold">{(100 - sessionData.currentUsage).toFixed(1)}%</div>
        </div>
        <div className="bg-white p-4 rounded shadow">
          <div className="text-sm text-gray-500">Margin to Warning</div>
          <div className="text-2xl font-bold">{(sessionData.warningThreshold - sessionData.currentUsage).toFixed(1)}%</div>
        </div>
      </div>

      {/* Add Operation Buttons */}
      <div className="flex gap-4 mb-6 flex-wrap">
        <button 
          onClick={handleAddOperation} 
          className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
        >
          Simulate Code Generation
        </button>
        <button 
          onClick={handleAddDiscussion} 
          className="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
        >
          Simulate Discussion
        </button>
        <button 
          onClick={handleAddArtifact} 
          className="bg-purple-500 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded"
        >
          Simulate Artifact Creation
        </button>
        <button 
          onClick={handleAddSearch} 
          className="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded"
        >
          Simulate Search Operation
        </button>
      </div>

      {/* Operations Table */}
      <div className="mb-6">
        <h2 className="text-lg font-semibold mb-2">Operation Tracking</h2>
        <div className="bg-white rounded shadow overflow-hidden">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Operation</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Details</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Usage %</th>
                <th className="px-4 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Cumulative %</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {sessionData.operations.map((op, index) => (
                <tr key={index} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="px-4 py-2 whitespace-nowrap text-sm font-medium text-gray-900">{op.type}</td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{op.details}</td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">{op.usage.toFixed(1)}%</td>
                  <td className="px-4 py-2 whitespace-nowrap text-sm text-gray-500">
                    <div className="flex items-center">
                      <span className="mr-2">{op.cumulative.toFixed(1)}%</span>
                      <div className="w-16 bg-gray-200 rounded-full h-2">
                        <div className={`${getGaugeColor(op.cumulative)} h-2 rounded-full`} style={{ width: `${op.cumulative}%` }}></div>
                      </div>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Recommendations */}
      <div className="bg-white p-4 rounded shadow mb-6">
        <h2 className="text-lg font-semibold mb-2">Recommendations</h2>
        <ul className="list-disc pl-5">
          {sessionData.recommendations.map((rec, index) => (
            <li key={index} className="text-sm text-gray-700 mb-1">{rec}</li>
          ))}
        </ul>
      </div>

      {/* Quick Reference */}
      <div className="mb-4">
        <h2 className="text-lg font-semibold mb-2">Operation Cost Quick Reference</h2>
        <div className="bg-white p-4 rounded shadow">
          <h3 className="font-medium mb-2">Code Generation (Base Cost × Size Factor)</h3>
          <div className="grid grid-cols-4 gap-2 mb-2 text-sm">
            <div className="font-medium">Complexity</div>
            <div>Low: {operationCosts.codeGeneration.base.low}%</div>
            <div>Medium: {operationCosts.codeGeneration.base.medium}%</div>
            <div>High: {operationCosts.codeGeneration.base.high}%</div>
          </div>
          <div className="grid grid-cols-4 gap-2 mb-2 text-sm">
            <div className="font-medium">Size Factor</div>
            <div>Small: {operationCosts.codeGeneration.sizeFactor.small}×</div>
            <div>Medium: {operationCosts.codeGeneration.sizeFactor.medium}×</div>
            <div>Large: {operationCosts.codeGeneration.sizeFactor.large}×</div>
          </div>

          <h3 className="font-medium mb-2 mt-4">Artifact Creation (Base Cost × Size Factor)</h3>
          <div className="grid grid-cols-4 gap-2 mb-2 text-sm">
            <div className="font-medium">Complexity</div>
            <div>Low: {operationCosts.artifactCreation.base.low}%</div>
            <div>Medium: {operationCosts.artifactCreation.base.medium}%</div>
            <div>High: {operationCosts.artifactCreation.base.high}%</div>
          </div>
          <div className="grid grid-cols-4 gap-2 mb-2 text-sm">
            <div className="font-medium">Size Factor</div>
            <div>Small: {operationCosts.artifactCreation.sizeFactor.small}×</div>
            <div>Medium: {operationCosts.artifactCreation.sizeFactor.medium}×</div>
            <div>Large: {operationCosts.artifactCreation.sizeFactor.large}×</div>
          </div>

          <h3 className="font-medium mb-2 mt-4">Other Operations</h3>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>Context Loading: {operationCosts.contextLoading.base}% + {operationCosts.contextLoading.perKb}% per KB</div>
            <div>Discussion Exchange: {operationCosts.discussionExchange.base}% + {operationCosts.discussionExchange.perWord}% per word</div>
            <div>Search Operation: {operationCosts.searchOperation.base}% + {operationCosts.searchOperation.perResult}% per result</div>
          </div>
        </div>
      </div>

      <div className="text-center text-xs text-gray-500 mt-4">
        TeamBadass Observable Gas Gauge System · Updated May 1, 2025
      </div>
    </div>
  );
}

export default GasGaugeDashboard;
