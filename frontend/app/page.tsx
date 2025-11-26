import {createClient} from '@supabase/supabase-js'


// initalize supabase
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

// runs on server every time i load page
async function getDecisions(){

  if(!process.env.NEXT_PUBLIC_SUPABASE_URL){
    console.error("Error: Supabase URL is missing")
  }


  const {data, error} = await supabase
    .from('decisions')
    .select('*')
    .order('created_at', {ascending:false});

    if(error){
      console.error("Supabase error:", error.message, error.details)
      return [];
    }

    console.log("Success, rows found:", data?.length);
    return data || [];

}



export default async function Home(){
  const decisions = await getDecisions();
  return (
    <div className="min-h-screen bg-gray-900 text-white p-10">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-blue-400">
          🔒 ThreadLock Dashboard
        </h1>

        <div className="space-y-4">
          {decisions.map((decision) => (
            <div 
              key={decision.id} 
              className="bg-gray-800 p-6 rounded-lg border border-gray-700 shadow-lg"
            >
              <div className="flex justify-between items-start mb-2">
                <h2 className="text-xl font-semibold text-green-400">
                  {decision.decision_text}
                </h2>
                <span className="text-xs text-gray-500">
                  {new Date(decision.created_at).toLocaleDateString()}
                </span>
              </div>
              
              <p className="text-gray-300 mb-4">
                {decision.rationale}
              </p>

              <div className="text-sm text-gray-500 font-mono bg-gray-900 p-2 rounded">
                Ticket Context: {decision.slack_thread_ts || 'N/A'}
              </div>
            </div>
          ))}

          {decisions.length === 0 && (
            <p className="text-center text-gray-500">No decisions found yet.</p>
          )}
        </div>
      </div>
    </div>
  );
}