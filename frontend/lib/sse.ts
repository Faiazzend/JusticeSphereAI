import { AgentDebateMessage } from './types';

export function connectDebateStream(
  contractId: string,
  onMessage: (message: AgentDebateMessage) => void,
  onComplete?: () => void,
  onError?: (err: any) => void
): () => void {
  const host = typeof window !== 'undefined' ? (window.location.hostname || '127.0.0.1') : '127.0.0.1';
  const url = process.env.NEXT_PUBLIC_API_URL 
    ? `${process.env.NEXT_PUBLIC_API_URL}/api/v1/stream/${contractId}`
    : `http://${host}:8000/api/v1/stream/${contractId}`;

  const eventSource = new EventSource(url);

  eventSource.onmessage = (event) => {
    try {
      const data = JSON.parse(event.data);
      if (data.event === 'agent_turn') {
        onMessage({
          index: data.index,
          agent_name: data.agent_name,
          timestamp: data.timestamp,
          content: data.content,
          target_clause: data.target_clause,
        });
      } else if (data.event === 'completed') {
        if (onComplete) onComplete();
        eventSource.close();
      }
    } catch (err) {
      console.error('Error parsing SSE event data', err);
    }
  };

  eventSource.onerror = (err) => {
    if (onError) onError(err);
    eventSource.close();
  };

  // Return unsubscribe/cleanup function
  return () => {
    eventSource.close();
  };
}
