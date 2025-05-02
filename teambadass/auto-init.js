/**
 * TeamBadass Auto-Initialization System
 * Minimal overhead, maximum functionality
 */

const fsHelper = require('./utils/fs-helper');
const gasTracker = require('./memory/gas-tracker');

class AutoInit {
    constructor(options = {}) {
        this.options = {
            mobile: false,
            minimal: false,
            verbose: true,
            ...options
        };

        this.repository = {
            detected: false,
            path: '/home/louthenw/Documents/teambadass_github/teambadass',
            fingerprint: null
        };

        this.initialized = {
            gas: false,
            memory: false
        };

        this.gasTracker = gasTracker;
    }

    async initialize() {
        // 1. Detect repository
        const repoDetected = await this.detectRepository();
        if (!repoDetected) {
            return { status: 'error', message: 'Repository not detected' };
        }

        // 2. Initialize gas tracking (silent)
        const gasResult = await this.initializeGas();

        // 3. Load minimal memory files
        const memoryResult = await this.loadMemory();

        // 4. Return initialization status
        return {
            status: 'success',
            gas: gasResult,
            memory: memoryResult,
            message: this.formatStatusMessage(gasResult, memoryResult)
        };
    }

    async detectRepository() {
        try {
            // Check for key files that indicate TeamBadass repository
            const keystoneExists = await fsHelper.pathExists(`${this.repository.path}/keystone`);
            const memoryExists = await fsHelper.pathExists(`${this.repository.path}/memory`);
            const gasExists = await fsHelper.pathExists(`${this.repository.path}/gas`);

            this.repository.detected = keystoneExists && memoryExists && gasExists;

            if (this.repository.detected) {
                // Generate fingerprint of key files
                this.repository.fingerprint = new Date().toISOString();
            }

            return this.repository.detected;
        } catch (error) {
            console.error(`Repository detection error: ${error}`);
            return false;
        }
    }

    async initializeGas() {
        try {
            // Initialize gas tracker silently
            const result = await this.gasTracker.initialize();

            // Register context loading
            this.gasTracker.recordOperation('contextLoading', { kb: 80 });

            this.initialized.gas = true;

            return {
                status: 'success',
                level: result.currentUsage || 0
            };
        } catch (error) {
            console.error(`Gas initialization error: ${error}`);
            return {
                status: 'error',
                message: error.message
            };
        }
    }

    async loadMemory() {
        try {
            // Define essential memory files
            const essentialFiles = [
                `${this.repository.path}/memory/core/team-dynamics-json.json`,
                `${this.repository.path}/memory/core/project-history-json.json`
            ];

            // Load essential files only
            const loadedFiles = [];
            for (const file of essentialFiles) {
                if (await fsHelper.pathExists(file)) {
                    // In a real implementation, we would process the file content
                    loadedFiles.push(file);
                }
            }

            this.initialized.memory = loadedFiles.length > 0;

            return {
                status: 'success',
                filesLoaded: loadedFiles.length,
                filesTotal: essentialFiles.length
            };
        } catch (error) {
            console.error(`Memory loading error: ${error}`);
            return {
                status: 'error',
                message: error.message
            };
        }
    }

    formatStatusMessage(gasResult, memoryResult) {
        if (this.options.minimal) {
            return `TeamBadass ready | Gas: ${gasResult.level}% | Memory: ${memoryResult.filesLoaded}/${memoryResult.filesTotal}`;
        }

        return `
        TeamBadass Auto-Initialization Complete
        - Gas Tracking: ${gasResult.status === 'success' ? '✅' : '❌'} (${gasResult.level}%)
        - Memory System: ${memoryResult.status === 'success' ? '✅' : '❌'} (${memoryResult.filesLoaded}/${memoryResult.filesTotal})
        `.trim();
    }

    // Repository optimization functions

    async getStorageAnalysis() {
        try {
            const result = {
                gas: { size: 0, files: 0 },
                keystone: { size: 0, files: 0 },
                memory: { size: 0, files: 0 },
                utils: { size: 0, files: 0 },
                other: { size: 0, files: 0 },
                total: { size: 0, files: 0 }
            };

            // Create list of directories to check
            const directories = [
                { path: `${this.repository.path}/gas`, category: 'gas' },
                { path: `${this.repository.path}/keystone`, category: 'keystone' },
                { path: `${this.repository.path}/memory`, category: 'memory' },
                { path: `${this.repository.path}/utils`, category: 'utils' }
            ];

            // Process each directory
            for (const dir of directories) {
                const stats = await this.getDirectoryStats(dir.path);
                result[dir.category] = stats;
                result.total.size += stats.size;
                result.total.files += stats.files;
            }

            // Calculate percentages
            Object.keys(result).forEach(key => {
                if (key !== 'total') {
                    result[key].percentage = Math.round((result[key].size / result.total.size) * 100);
                }
            });

            return result;
        } catch (error) {
            console.error(`Storage analysis error: ${error}`);
            return null;
        }
    }

    async getDirectoryStats(dirPath) {
        try {
            // This would use the fs.list_directory and fs.get_file_info functions
            // Simplified implementation for now
            return { size: 0, files: 0 };
        } catch (error) {
            console.error(`Directory stats error: ${error}`);
            return { size: 0, files: 0 };
        }
    }

    async createOptimizationPlan() {
        const analysis = await this.getStorageAnalysis();

        return {
            analysis,
            phases: [
                {
                    name: 'Gas Consolidation',
                    description: 'Consolidate gas tracking implementations',
                    potentialSavings: '15%',
                    files: {
                        keep: [
                            `${this.repository.path}/gas/minimal-tracker.py`,
                            `${this.repository.path}/gas/README.md`
                        ],
                        delete: [
                            `${this.repository.path}/gas/gas_gauge_core.py`,
                            `${this.repository.path}/gas/gauge_reporting.py`,
                            `${this.repository.path}/gas/dashboard.tsx`
                        ]
                    }
                },
                {
                    name: 'Memory Consolidation',
                    description: 'Streamline memory system implementations',
                    potentialSavings: '8%',
                    files: {
                        keep: [
                            `${this.repository.path}/memory/core.js`,
                            `${this.repository.path}/memory/gas-tracker.js`,
                            `${this.repository.path}/memory/config/system.json`
                        ],
                        move: [
                            // Files to move to config directory
                            { from: `${this.repository.path}/memory/bootstrap.json`, to: `${this.repository.path}/memory/config/bootstrap.json` }
                        ]
                    }
                },
                {
                    name: 'Keystone Optimization',
                    description: 'Move keystones to separate repository',
                    potentialSavings: '19%',
                    newRepo: '/home/louthenw/Documents/teambadass_keystone'
                }
            ]
        };
    }
}

module.exports = new AutoInit();

// Example usage:
// const autoInit = require('./auto-init');
// autoInit.initialize().then(result => console.log(result));
