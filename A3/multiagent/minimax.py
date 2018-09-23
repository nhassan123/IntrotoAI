      
        "*** YOUR CODE HERE ***"
        maxGhosts = gameState.getNumAgents() - 1
        
        def maxValue(state, depth, numghosts):
            maxval = -(float("inf"))
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(state)
                
            
            
            actions = state.getLegalActions(0)
            
            for action in actions:
                maxval = max(maxval,minValue(state.generateSuccessor(0,action),depth-1,1,numghosts))
                #maxval = max(value, maxval)
            
            return maxval
            
        def minValue(state,depth,agent,ghosts):
            minval = float("inf")
            
            if state.isWin() or state.isLose() or depth ==0:
                return self.evaluationFunction(state)
                
            
            actions = state.getLegalActions(agent)
            if agent == ghosts:
                for action in actions:
                    minval = min(minval, maxValue(state.generateSuccessor(agent, action), depth-1, ghosts))
            else:
                for action in actions:
                    minval =  min(minval, minValue(state.generateSuccessor(agent,action), depth, agent +1, ghosts))
                    #minval = min(minval,value)
            return minval
            

        '''def maxvalue(gameState, depth, numghosts):
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = -(float("inf"))
            legalActions = gameState.getLegalActions(0)
            for action in legalActions:
                v = max(v, minvalue(gameState.generateSuccessor(0, action), depth - 1, 1, numghosts))
            return v
        
        def minvalue(gameState, depth, agentindex, numghosts):
            "numghosts = len(gameState.getGhostStates())"
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(gameState)
            v = float("inf")
            legalActions = gameState.getLegalActions(agentindex)
            if agentindex == numghosts:
                for action in legalActions:
                    v = min(v, maxvalue(gameState.generateSuccessor(agentindex, action), depth - 1, numghosts))
            else:
                for action in legalActions:
                    v = min(v, minvalue(gameState.generateSuccessor(agentindex, action), depth, agentindex + 1, numghosts))
            return v'''
            
        legalActions = gameState.getLegalActions()
        numghosts = gameState.getNumAgents() - 1
        bestaction = Directions.STOP
        score = -(float("inf"))
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            prevscore = score
            score = max(score, minValue(nextState, self.depth, 1, numghosts))
            if score > prevscore:
                bestaction = action
        return bestaction
                
    
evaluate = self.evaluationFunction
    
    maxDepth = self.depth
    maxGhosts = gameState.getNumAgents() - 1
    
    
        evaluate = self.evaluationFunction
            
        maxDepth = self.depth
        maxGhosts = gameState.getNumAgents() - 1


        def maxValue(state, depth):
            """
            The Pacman maximizing utility function. 
            """
            if depth >= maxDepth or state.isWin() or state.isLose():
                # Terminal condition to leave
                utility = evaluate(state)
                return utility
            
            # The worst thing a Pacman can do is to be idle without doing anything.
            u = float('-inf')
            
            depth += 1
            # We filter the stop action as it is already defined as the possible initial state
            actions = [ action for action in state.getLegalActions() if action != Directions.STOP ]
            for action in actions:
                # For each of the action the Pacman can perform, generate a new state
                # with such action executed, and imagine how the ghosts would behave
                # and minimize pacman's utility value
                utility = minValue(state.generateSuccessor(0, action), depth)
                u = max(u, utility)
            return u
    
        def minValue(state, depth, ghost_id = None):
            """
            The Ghosts minimizing utility function
            """
            if depth >= maxDepth or state.isWin() or state.isLose():
                # Terminal condition to leave
                utility = evaluate(state)
                return utility
            
            if ghost_id == None:
                ghost_id = 1
            next_ghost_id = ghost_id + 1
            
            # So why initialize the ghost minimizing utility to these
            # values? The best thing a ghost can do to maximize the
            # pacman's utility would be to be frozen, and quiet.
            # Though that won't happen ever...
            u = float('inf')
            
            # For each ghost, iterate over each of its actions
            # to calculate the utility of the new generated state
            for action in state.getLegalActions(ghost_id):
                # Always find the minimal utility value of the Pacman.
                # We don't want that pesky guy to win over our ghosts.
                if ghost_id == maxGhosts:
                    utility = maxValue(state.generateSuccessor(ghost_id, action), depth)
                else:
                    utility = minValue(state.generateSuccessor(ghost_id, action), depth, next_ghost_id)
                    u = min(u, utility)
            return u
    
        actions = [ action for action in gameState.getLegalActions() if action != Directions.STOP ]
        actions_utilities = []
        for action in actions:
            actions_utilities.append((minValue(gameState.generateSuccessor(0, action), 1), action))
        
        best_action = max(actions_utilities)
        
        return best_action[1]
        
        ####
        
        maxGhosts = gameState.getNumAgents() - 1
        
        def maxValue(state, depth, numghosts):
            maxval = -(float("inf"))
            if gameState.isWin() or gameState.isLose() or depth == 0:
                return self.evaluationFunction(state)
                
            actions = state.getLegalActions(0)
            
            for action in actions:
                maxval = max(maxval,minValue(state.generateSuccessor(0,action),depth,1,numghosts))
                #maxval = max(value, maxval)
            
            return maxval
            
        def minValue(state,depth,agent,ghosts):
            minval = float("inf")
            
            if state.isWin() or state.isLose() or depth ==0:
                return self.evaluationFunction(state)
                
            
            actions = state.getLegalActions(agent)
            if agent == ghosts:
                for action in actions:
                    minval = min(minval, maxValue(state.generateSuccessor(agent, action), depth-1, ghosts))
            else:
                for action in actions:
                    minval =  min(minval, minValue(state.generateSuccessor(agent,action), depth, agent +1, ghosts))
                    #minval = min(minval,value)
            return minval
            

        legalActions = gameState.getLegalActions()
        numghosts = gameState.getNumAgents() - 1
        bestaction = legalActions[0]
        score = -(float("inf"))
        for action in legalActions:
            nextState = gameState.generateSuccessor(0, action)
            prevscore = score
            score = max(score, minValue(nextState, self.depth, 1, numghosts))
            if score > prevscore:
                bestaction = action
        return bestaction
