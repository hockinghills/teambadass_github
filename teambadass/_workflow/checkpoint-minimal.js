/**
 * TeamBadass Minimal Checkpoint System
 * Ultralight implementation for tracking progress
 */

class CheckpointSystem {
  constructor(options = {}) {
    this.filePath = options.filePath || './checkpoint.json';
    this.project = options.project || 'default';
    this.data = {
      project: this.project,
      updated: new Date().toISOString(),
      completed: [],
      pending: [],
      next: null
    };
  }

  async init() {
    try {
      // Try to load existing checkpoint
      const content = await fs.read_file({path: this.filePath});
      this.data = JSON.parse(content);
      return true;
    } catch (error) {
      // Create new checkpoint file
      return this.save();
    }
  }

  async save() {
    this.data.updated = new Date().toISOString();
    await fs.write_file({
      path: this.filePath,
      content: JSON.stringify(this.data, null, 2)
    });
    return true;
  }

  async setPlan(componentList) {
    // Filter already completed components
    this.data.pending = componentList.filter(
      c => !this.data.completed.includes(c)
    );
    
    // Set next component if there are pending components
    this.data.next = this.data.pending.length > 0 ? 
      this.data.pending[0] : null;
    
    return this.save();
  }

  async complete(componentName) {
    // Move from pending to completed
    const index = this.data.pending.indexOf(componentName);
    if (index > -1) {
      this.data.pending.splice(index, 1);
    }
    
    // Add to completed if not already there
    if (!this.data.completed.includes(componentName)) {
      this.data.completed.push(componentName);
    }
    
    // Update next component
    this.data.next = this.data.pending.length > 0 ? 
      this.data.pending[0] : null;
    
    return this.save();
  }

  isCompleted(componentName) {
    return this.data.completed.includes(componentName);
  }

  getNext() {
    return this.data.next;
  }

  getStatus() {
    const total = this.data.completed.length + this.data.pending.length;
    const progress = total > 0 ? 
      Math.round((this.data.completed.length / total) * 100) : 0;
    
    return {
      project: this.data.project,
      progress: progress,
      completed: this.data.completed.length,
      pending: this.data.pending.length,
      next: this.data.next
    };
  }
}

module.exports = CheckpointSystem;