import React, { useState, useEffect } from 'react';

const RepoMaintenanceTracker = () => {
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [stats, setStats] = useState({ total: 0, needsToc: 0, delete: 0, update: 0 });

  // Initial file data based on repository structure
  useEffect(() => {
    // Normally we'd fetch this from an API, but we'll use static data for now
    const repoFiles = [
      { 
        path: 'teambadass/_memory/gas_gauge/gas_gauge_core.py', 
        hasToc: false, 
        status: 'needsToc', 
        type: 'py', 
        lastUpdated: '2025-05-01',
        gasSavings: 'high'
      },
      { 
        path: 'teambadass/_memory/gas_gauge/gauge_reporting.py', 
        hasToc: false, 
        status: 'needsToc', 
        type: 'py',
        lastUpdated: '2025-05-01',
        gasSavings: 'high'
      },
      { 
        path: 'teambadass/_memory/gas_gauge/observable_gas_gauge.py', 
        hasToc: false, 
        status: 'update', 
        type: 'py',
        lastUpdated: '2025-05-01',
        gasSavings: 'high'
      },
      { 
        path: 'teambadass/_memory/gas_gauge/dashboard.html', 
        hasToc: false, 
        status: 'delete', 
        type: 'html',
        lastUpdated: '2025-05-01',
        gasSavings: 'low'
      },
      { 
        path: 'teambadass/_memory/gas_gauge/dashboard.jsx', 
        hasToc: false, 
        status: 'update', 
        type: 'jsx',
        lastUpdated: '2025-05-01',
        gasSavings: 'medium'
      },
      { 
        path: 'teambadass/_memory/gas_gauge/dashboard.tsx', 
        hasToc: false, 
        status: 'keep', 
        type: 'tsx',
        lastUpdated: '2025-05-01',
        gasSavings: 'low'
      },
      { 
        path: 'teambadass/_memory/core/team-dynamics-json.json', 
        hasToc: false, 
        status: 'needsToc', 
        type: 'json',
        lastUpdated: '2025-04-28',
        gasSavings: 'high'
      },
      { 
        path: 'teambadass/_memory/core/project-history-json.json', 
        hasToc: false, 
        status: 'needsToc', 
        type: 'json',
        lastUpdated: '2025-04-29',
        gasSavings: 'high'
      },
      { 
        path: 'teambadass/_memory/gas_gauge/auto_init.py', 
        hasToc: true, 
        status: 'keep', 
        type: 'py',
        lastUpdated: '2025-05-01',
        gasSavings: 'complete'
      },
      { 
        path: 'teambadass/_memory/gas_gauge/mobile_integration.py', 
        hasToc: true, 
        status: 'keep', 
        type: 'py',
        lastUpdated: '2025-05-01',
        gasSavings: 'complete'
      },
      { 
        path: 'teambadass/_memory/init.py', 
        hasToc: true, 
        status: 'keep', 
        type: 'py',
        lastUpdated: '2025-05-01',
        gasSavings: 'complete'
      },
      { 
        path: 'teambadass/README.md', 
        hasToc: false, 
        status: 'needsToc', 
        type: 'md',
        lastUpdated: '2025-04-28',
        gasSavings: 'medium'
      },
      { 
        path: 'teambadass/_memory/gas_gauge/operation-tracking-model.js', 
        hasToc: false, 
        status: 'needsToc', 
        type: 'js',
        lastUpdated: '2025-05-01',
        gasSavings: 'high'
      },
      { 
        path: 'teambadass/_memory/system/claude_gas_gauge.py', 
        hasToc: false, 
        status: 'delete', 
        type: 'py',
        lastUpdated: '2025-04-28',
        gasSavings: 'duplicate'
      },
      { 
        path: 'teambadass/_memory/system/session_start.py', 
        hasToc: false, 
        status: 'delete', 
        type: 'py',
        lastUpdated: '2025-04-28',
        gasSavings: 'duplicate'
      }
    ];

    setFiles(repoFiles);
    setLoading(false);

    // Calculate statistics
    const total = repoFiles.length;
    const needsToc = repoFiles.filter(f => f.status === 'needsToc').length;
    const deleteCount = repoFiles.filter(f => f.status === 'delete').length;
    const updateCount = repoFiles.filter(f => f.status === 'update').length;
    
    setStats({
      total,
      needsToc,
      delete: deleteCount,
      update: updateCount,
      potential: Math.round((needsToc * 0.1 + updateCount * 0.05) * 100) // Estimated gas savings %
    });
  }, []);

  // Filter files based on selected filter and search term
  const filteredFiles = files.filter(file => {
    const matchesFilter = filter === 'all' || file.status === filter;
    const matchesSearch = file.path.toLowerCase().includes(searchTerm.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  // Update file status
  const updateFileStatus = (path, newStatus) => {
    const updatedFiles = files.map(file => 
      file.path === path ? { ...file, status: newStatus } : file
    );
    setFiles(updatedFiles);
    
    // Update statistics
    const needsToc = updatedFiles.filter(f => f.status === 'needsToc').length;
    const deleteCount = updatedFiles.filter(f => f.status === 'delete').length;
    const updateCount = updatedFiles.filter(f => f.status === 'update').length;
    
    setStats({
      ...stats,
      needsToc,
      delete: deleteCount,
      update: updateCount,
      potential: Math.round((needsToc * 0.1 + updateCount * 0.05) * 100)
    });
  };

  // Get color based on status
  const getStatusColor = (status) => {
    switch(status) {
      case 'needsToc': return 'bg-yellow-100 border-yellow-500';
      case 'delete': return 'bg-red-100 border-red-500';
      case 'update': return 'bg-blue-100 border-blue-500';
      case 'keep': return 'bg-green-100 border-green-500';
      default: return 'bg-gray-100 border-gray-500';
    }
  };

  // Get emoji and label for file status
  const getStatusInfo = (status) => {
    switch(status) {
      case 'needsToc': return { emoji: '📑', label: 'Needs TOC' };
      case 'delete': return { emoji: '🗑️', label: 'Delete' };
      case 'update': return { emoji: '🔄', label: 'Update' };
      case 'keep': return { emoji: '✅', label: 'Keep' };
      default: return { emoji: '❓', label: 'Unknown' };
    }
  };

  // Get savings emoji
  const getSavingsEmoji = (savings) => {
    switch(savings) {
      case 'high': return '💰💰💰';
      case 'medium': return '💰💰';
      case 'low': return '💰';
      case 'complete': return '✅';
      case 'duplicate': return '🔄';
      default: return '';
    }
  };

  if (loading) {
    return <div className="p-4">Loading repository files...</div>;
  }

  return (
    <div className="max-w-full p-2">
      <div className="mb-4">
        <h1 className="text-lg font-bold mb-2">Repository Maintenance</h1>
        
        {/* Stats summary */}
        <div className="grid grid-cols-2 gap-2 mb-4">
          <div className="bg-white p-2 rounded shadow">
            <div className="text-sm text-gray-600">Needs TOC</div>
            <div className="text-xl font-bold">{stats.needsToc}/{stats.total}</div>
          </div>
          <div className="bg-white p-2 rounded shadow">
            <div className="text-sm text-gray-600">To Delete</div>
            <div className="text-xl font-bold">{stats.delete}/{stats.total}</div>
          </div>
          <div className="bg-white p-2 rounded shadow">
            <div className="text-sm text-gray-600">To Update</div>
            <div className="text-xl font-bold">{stats.update}/{stats.total}</div>
          </div>
          <div className="bg-white p-2 rounded shadow">
            <div className="text-sm text-gray-600">Potential Savings</div>
            <div className="text-xl font-bold">{stats.potential}%</div>
          </div>
        </div>
        
        {/* Filter and search */}
        <div className="flex flex-col gap-2 mb-4">
          <div className="flex space-x-1">
            <button 
              onClick={() => setFilter('all')} 
              className={`px-2 py-1 text-xs rounded ${filter === 'all' ? 'bg-gray-700 text-white' : 'bg-gray-200'}`}
            >
              All
            </button>
            <button 
              onClick={() => setFilter('needsToc')} 
              className={`px-2 py-1 text-xs rounded ${filter === 'needsToc' ? 'bg-yellow-500 text-white' : 'bg-yellow-100'}`}
            >
              📑 Needs TOC
            </button>
            <button 
              onClick={() => setFilter('delete')} 
              className={`px-2 py-1 text-xs rounded ${filter === 'delete' ? 'bg-red-500 text-white' : 'bg-red-100'}`}
            >
              🗑️ Delete
            </button>
            <button 
              onClick={() => setFilter('update')} 
              className={`px-2 py-1 text-xs rounded ${filter === 'update' ? 'bg-blue-500 text-white' : 'bg-blue-100'}`}
            >
              🔄 Update
            </button>
            <button 
              onClick={() => setFilter('keep')} 
              className={`px-2 py-1 text-xs rounded ${filter === 'keep' ? 'bg-green-500 text-white' : 'bg-green-100'}`}
            >
              ✅ Keep
            </button>
          </div>
          <input
            type="text"
            placeholder="Search files..."
            className="w-full p-2 border rounded"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </div>

      {/* File list */}
      <div className="space-y-2">
        {filteredFiles.length === 0 ? (
          <div className="text-center p-4">No files match your criteria</div>
        ) : (
          filteredFiles.map((file) => {
            const statusInfo = getStatusInfo(file.status);
            
            return (
              <div 
                key={file.path}
                className={`border-l-4 p-2 rounded ${getStatusColor(file.status)}`}
              >
                <div className="flex justify-between items-start">
                  <div>
                    <div className="font-bold text-sm break-all">
                      {file.path.split('/').pop()}
                    </div>
                    <div className="text-xs text-gray-600 break-all">
                      {file.path}
                    </div>
                    <div className="flex gap-2 mt-1">
                      <span className="text-xs bg-gray-200 px-1 rounded">
                        {file.type}
                      </span>
                      <span className="text-xs bg-gray-200 px-1 rounded">
                        {file.lastUpdated}
                      </span>
                      <span className="text-xs bg-gray-200 px-1 rounded">
                        Savings: {getSavingsEmoji(file.gasSavings)}
                      </span>
                    </div>
                  </div>
                  <div className="text-xs font-bold">
                    {statusInfo.emoji} {statusInfo.label}
                  </div>
                </div>
                
                {/* Actions */}
                <div className="flex gap-1 mt-2">
                  <button 
                    onClick={() => updateFileStatus(file.path, 'needsToc')}
                    className="text-xs px-2 py-1 bg-yellow-100 rounded hover:bg-yellow-200"
                  >
                    📑 TOC
                  </button>
                  <button 
                    onClick={() => updateFileStatus(file.path, 'delete')}
                    className="text-xs px-2 py-1 bg-red-100 rounded hover:bg-red-200"
                  >
                    🗑️ Delete
                  </button>
                  <button 
                    onClick={() => updateFileStatus(file.path, 'update')}
                    className="text-xs px-2 py-1 bg-blue-100 rounded hover:bg-blue-200"
                  >
                    🔄 Update
                  </button>
                  <button 
                    onClick={() => updateFileStatus(file.path, 'keep')}
                    className="text-xs px-2 py-1 bg-green-100 rounded hover:bg-green-200"
                  >
                    ✅ Keep
                  </button>
                </div>
              </div>
            );
          })
        )}
      </div>

      {/* Summary box */}
      <div className="mt-4 p-2 bg-gray-100 rounded">
        <h2 className="font-bold text-sm">Next Steps</h2>
        <ul className="text-xs list-disc pl-4 mt-1">
          <li>Add TOC to {stats.needsToc} files (~{stats.needsToc * 10}% gas savings)</li>
          <li>Remove {stats.delete} duplicate/obsolete files</li>
          <li>Update {stats.update} files with improved implementations</li>
          <li>Potential total gas savings: ~{stats.potential}%</li>
        </ul>
      </div>
    </div>
  );
};

export default RepoMaintenanceTracker;
